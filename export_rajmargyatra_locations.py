#!/usr/bin/env python3
"""Export a compact plaza-location CSV from the official Rajmargyatra payload."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "raw" / "rajmargyatra" / "official_plaza_details.json"
OUTPUT = ROOT / "processed" / "rajmargyatra_plaza_locations.csv"

FIELDS = {
    "tollplaza_id": "tollplaza_id",
    "tollplaza_code": "tollplaza_code",
    "tollplaza_name": "tollplaza_name",
    "state_name": "state_name",
    "nh_no": "nh_no",
    "location": "Location",
    "latitude": "latitude",
    "longitude": "longitude",
    "piu": "piu",
    "ro": "ro",
    "active": "active",
}


def main() -> None:
    raw = json.loads(SOURCE.read_text())
    records = []
    for row in raw:
        record = {}
        for output_name, source_name in FIELDS.items():
            value = row.get(source_name)
            if output_name in {"piu", "ro"} and isinstance(value, list):
                value = "; ".join(
                    str(item.get(output_name, "")).strip()
                    for item in value
                    if item.get(output_name)
                )
            record[output_name] = " ".join(value.split()) if isinstance(value, str) else value
        records.append(record)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    print(f"Exported {len(records):,} plaza locations to {OUTPUT}")


if __name__ == "__main__":
    main()
