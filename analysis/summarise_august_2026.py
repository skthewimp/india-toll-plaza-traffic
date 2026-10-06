#!/usr/bin/env python3
"""Print the headline August 2026 heavy-vehicle traffic findings."""

from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "processed" / "ihmcl_vehicle_class_august_2026.csv"


def percentage(value: float) -> str:
    return f"{value:.1%}"


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE

    with source.open() as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        row["total_cnt"] = int(row["total_cnt"])
        row["heavy_vehicle_count"] = int(row["heavy_vehicle_count"])
        row["heavy_vehicle_crossings_per_day"] = float(
            row["heavy_vehicle_crossings_per_day"]
        )

    total_crossings = sum(row["total_cnt"] for row in rows)
    heavy_crossings = sum(row["heavy_vehicle_count"] for row in rows)
    daily_values = [row["heavy_vehicle_crossings_per_day"] for row in rows]
    ranked = sorted(
        rows,
        key=lambda row: row["heavy_vehicle_count"],
        reverse=True,
    )

    ro_totals = defaultdict(int)
    for row in rows:
        ro_totals[row["ro"]] += row["heavy_vehicle_count"]

    print(f"Plazas: {len(rows):,}")
    print(f"All FASTag crossings: {total_crossings:,}")
    print(f"Heavy-vehicle crossings: {heavy_crossings:,}")
    print(f"Heavy share: {percentage(heavy_crossings / total_crossings)}")
    print(f"Heavy crossings per day: {heavy_crossings / 31:,.0f}")
    print(f"Median plaza per day: {statistics.median(daily_values):,.0f}")
    print(f"Mean plaza per day: {statistics.mean(daily_values):,.0f}")

    print("\nBusiest plazas")
    for row in ranked[:10]:
        print(
            f"{row['plaza_name']}: "
            f"{row['heavy_vehicle_crossings_per_day']:,.0f} per day"
        )

    print("\nConcentration")
    for count in (10, 25, 50, 100):
        subtotal = sum(row["heavy_vehicle_count"] for row in ranked[:count])
        print(f"Top {count}: {percentage(subtotal / heavy_crossings)}")

    print("\nRegional-office totals")
    for ro, crossings in sorted(
        ro_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:10]:
        print(f"{ro}: {crossings:,} ({percentage(crossings / heavy_crossings)})")


if __name__ == "__main__":
    main()
