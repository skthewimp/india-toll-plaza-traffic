#!/usr/bin/env python3
"""Extract IHMCL's August 2026 vehicle-class table from its source PDF."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "raw" / "ihmcl" / "monthly_vehicle_class" / "Aug-2026.pdf"
OUTPUT = ROOT / "processed" / "ihmcl_vehicle_class_august_2026.csv"

EXPECTED_COLUMNS = [
    "PLAZA_NAME",
    "PIU",
    "RO",
    "CAR_JEEP_CNT",
    "CAR_JEEP_AMT",
    "LCV_CNT",
    "LCV_AMT",
    "BUS_TRUCK_CNT",
    "BUS_TRUCK_AMT",
    "3_AXLE_CNT",
    "3_AXLE_AMT",
    "4_6_AXLE_CNT",
    "4_6_AXLE_AMT",
    "OSV_CNT",
    "OSV_AMT",
    "TOTAL_CNT",
    "TOTAL_AMT",
]

TEXT_COLUMNS = {"PLAZA_NAME", "PIU", "RO"}


def clean_number(value: str | None) -> int:
    """Parse Indian-formatted integers; IHMCL uses a dash for zero."""
    if value is None or value.strip() in {"", "-"}:
        return 0
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else 0


def extract_rows() -> list[dict[str, str | int]]:
    records = []

    with pdfplumber.open(SOURCE) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if len(tables) != 1:
                raise ValueError(f"Expected one table on page {page.page_number}")

            for row in tables[0]:
                if len(row) != len(EXPECTED_COLUMNS):
                    continue
                if row[0] in {"PLAZA_NAME", "VC Wise Monthly ETC FASTag Data for the Month of Aug 2026"}:
                    continue

                record = {}
                for column, value in zip(EXPECTED_COLUMNS, row):
                    if column in TEXT_COLUMNS:
                        record[column.lower()] = " ".join((value or "").split())
                    else:
                        record[column.lower()] = clean_number(value)

                record["heavy_vehicle_count"] = (
                    record["3_axle_cnt"]
                    + record["4_6_axle_cnt"]
                    + record["osv_cnt"]
                )
                record["heavy_vehicle_crossings_per_day"] = round(
                    record["heavy_vehicle_count"] / 31,
                    2,
                )
                records.append(record)

    return records


def main() -> None:
    records = extract_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Extracted {len(records):,} plaza rows to {OUTPUT}")
    print(
        "Heavy crossings:",
        f"{sum(row['heavy_vehicle_count'] for row in records):,}",
        "for August 2026",
    )


if __name__ == "__main__":
    main()
