#!/usr/bin/env python3
"""Download the public source files behind the toll-plaza traffic map."""

from __future__ import annotations

import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
IHMCL_DIR = ROOT / "raw" / "ihmcl"
RAJMARGYATRA_DIR = ROOT / "raw" / "rajmargyatra"
METADATA_DIR = ROOT / "metadata"

IHMCL_REPORTS_URL = "https://ihmcl.co.in/etc-transaction-reports/"
RAJMARGYATRA_API = "https://rajmargyatra.nhai.gov.in/nhai/api"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Referer": "https://rajmargyatra.nhai.gov.in/ataglance",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/140.0 Safari/537.36"
    ),
}


def download_file(session: requests.Session, url: str, destination: Path) -> str:
    """Download one file unless a non-empty copy is already present."""
    if destination.exists() and destination.stat().st_size > 0:
        return "already_present"

    partial = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(3):
        try:
            with session.get(url, timeout=(30, 300), stream=True) as response:
                response.raise_for_status()
                with partial.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
            partial.replace(destination)
            return "downloaded"
        except requests.RequestException as exc:
            if partial.exists():
                partial.unlink()
            if attempt == 2:
                return f"failed: {exc}"
            time.sleep(2 * (attempt + 1))

    return "failed"


def ihmcl_data_links(html: str) -> list[tuple[str, str, str]]:
    """Select transaction, annual-pass, and MLFF data links from the IHMCL page."""
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for anchor in soup.find_all("a", href=True):
        label = " ".join(anchor.get_text(" ", strip=True).split())
        url = anchor["href"]
        filename = Path(urlparse(url).path).name
        lower = filename.lower()

        is_historical_archive = lower.endswith(".zip") and "vcwise" in lower
        is_monthly_traffic = lower.endswith(".pdf") and any(
            marker in lower
            for marker in (
                "-2025",
                "-2026",
                "2025-etc-data",
                "2026-1",
            )
        ) and "annual-pass" not in lower
        is_annual_pass = "annual-pass-data" in lower
        is_mlff = "monthly_data" in lower or "mlff-plaza-data" in lower

        if not (is_historical_archive or is_monthly_traffic or is_annual_pass or is_mlff):
            continue

        category = (
            "historical_vehicle_class_archive"
            if is_historical_archive
            else "annual_pass"
            if is_annual_pass
            else "mlff"
            if is_mlff
            else "monthly_vehicle_class"
        )
        links.append((category, label, url))

    return list(dict.fromkeys(links))


def download_ihmcl_files() -> list[dict[str, str]]:
    session = requests.Session()
    session.headers.update({"User-Agent": HEADERS["User-Agent"]})

    html_path = METADATA_DIR / "ihmcl_etc_transaction_reports.html"
    if html_path.exists():
        html = html_path.read_text()
    else:
        response = session.get(IHMCL_REPORTS_URL, timeout=120)
        response.raise_for_status()
        html = response.text
        html_path.write_text(html)

    manifest = []
    for category, label, url in ihmcl_data_links(html):
        filename = Path(urlparse(url).path).name
        destination = IHMCL_DIR / category / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        status = download_file(session, url, destination)
        manifest.append(
            {
                "category": category,
                "label": label,
                "url": url,
                "local_path": str(destination.relative_to(ROOT)),
                "bytes": str(destination.stat().st_size) if destination.exists() else "0",
                "status": status,
            }
        )

    return manifest


def post_json(session: requests.Session, endpoint: str, payload: dict) -> dict:
    response = session.post(
        f"{RAJMARGYATRA_API}/{endpoint}",
        headers=HEADERS,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def fetch_plaza_detail(plaza: dict) -> tuple[int, dict | None, str | None]:
    plaza_id = plaza["tollplaza_id"]
    for attempt in range(4):
        try:
            with requests.Session() as session:
                response = post_json(
                    session,
                    "getTollplazaDetails",
                    {"tollplaza_id": plaza_id},
                )
            if response.get("resultCode") == 200 and response.get("payload"):
                return plaza_id, response["payload"][0], None
            error = response.get("resultString", "no payload")
        except requests.RequestException as exc:
            error = str(exc)
        time.sleep(1.5 * (attempt + 1))

    return plaza_id, None, error


def download_rajmargyatra() -> None:
    """Fetch the current official plaza list and full per-plaza detail payloads."""
    with requests.Session() as session:
        response = post_json(session, "getTollplazaName", {})

    plazas = response["payload"]
    list_path = RAJMARGYATRA_DIR / "official_plaza_list.json"
    list_path.write_text(json.dumps(plazas, indent=2, ensure_ascii=False))

    details_path = RAJMARGYATRA_DIR / "official_plaza_details.json"
    errors_path = RAJMARGYATRA_DIR / "official_plaza_detail_errors.json"

    existing = []
    if details_path.exists():
        existing = json.loads(details_path.read_text())
    details_by_id = {row["tollplaza_id"]: row for row in existing}

    pending = [row for row in plazas if row["tollplaza_id"] not in details_by_id]
    errors = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch_plaza_detail, plaza) for plaza in pending]
        for completed, future in enumerate(as_completed(futures), start=1):
            plaza_id, detail, error = future.result()
            if detail is not None:
                details_by_id[plaza_id] = detail
            else:
                errors.append({"tollplaza_id": plaza_id, "error": error})

            if completed % 50 == 0:
                details_path.write_text(
                    json.dumps(
                        list(details_by_id.values()),
                        indent=2,
                        ensure_ascii=False,
                    )
                )
                print(f"Rajmargyatra details: {len(details_by_id)}/{len(plazas)}")

    details_path.write_text(
        json.dumps(list(details_by_id.values()), indent=2, ensure_ascii=False)
    )
    errors_path.write_text(json.dumps(errors, indent=2, ensure_ascii=False))


def copy_open_mirror_snapshots() -> None:
    """Keep the open mirror's current and dated snapshots as reproducibility backups."""
    mirror_dir = RAJMARGYATRA_DIR / "open_mirror_snapshots"
    mirror_dir.mkdir(parents=True, exist_ok=True)

    base = "https://raw.githubusercontent.com/ForceGT/india-toll-plazas/main/data"
    snapshots = {
        "latest.json": f"{base}/latest.json",
        "nhai.json": f"{base}/sources/nhai.json",
        "2026-04-26_tollplazas.json": f"{base}/2026-04-26/tollplazas.json",
        "2026-04-30_tollplazas.json": f"{base}/2026-04-30/tollplazas.json",
        "05-2026_tollplazas.json": f"{base}/05-2026/tollplazas.json",
        "06-2026_tollplazas.json": f"{base}/06-2026/tollplazas.json",
        "07-2026_tollplazas.json": f"{base}/07-2026/tollplazas.json",
    }

    with requests.Session() as session:
        session.headers.update({"User-Agent": HEADERS["User-Agent"]})
        for filename, url in snapshots.items():
            download_file(session, url, mirror_dir / filename)


def write_manifest(rows: list[dict[str, str]]) -> None:
    manifest_path = METADATA_DIR / "ihmcl_download_manifest.csv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    (METADATA_DIR / "downloaded_at.txt").write_text(
        datetime.now().astimezone().isoformat(timespec="seconds") + "\n"
    )


def main() -> None:
    for directory in (IHMCL_DIR, RAJMARGYATRA_DIR, METADATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    manifest = download_ihmcl_files()
    write_manifest(manifest)
    download_rajmargyatra()
    copy_open_mirror_snapshots()


if __name__ == "__main__":
    main()
