# India toll-plaza traffic

Code and analytical notes for reproducing an August 2026 map of heavy-vehicle
crossings at Indian toll plazas.

The project combines two public sources:

- [IHMCL monthly FASTag reports](https://ihmcl.co.in/etc-transaction-reports/)
  for vehicle-class crossing counts.
- [NHAI Rajmargyatra](https://rajmargyatra.nhai.gov.in/) for toll-plaza
  coordinates and metadata.

No source or derived data is committed to this repository. The scripts download
it locally into ignored directories.

## What the code does

1. `download_sources.py` downloads all vehicle-class reports currently exposed
   by IHMCL, the live Rajmargyatra plaza payload, and several dated open-mirror
   snapshots.
2. `extract_august_2026.py` converts the August 2026 IHMCL PDF into a tidy CSV.
3. `export_rajmargyatra_locations.py` creates a compact location CSV from the
   official API payload.
4. `analysis/summarise_august_2026.py` reproduces the headline findings in
   [reports/initial-findings.md](reports/initial-findings.md).

Heavy vehicles follow the definition in the original map: three-axle vehicles,
four-to-six-axle vehicles, and oversized vehicles. The daily measure divides
August's monthly crossings by 31. These are crossing events, not unique trucks.

## Run it

Use Python 3.11 or later. On Karthik's machine, use the shared data-science
environment rather than creating a project environment.

```bash
uv pip install \
  --python /Users/Karthik/envs/datascience/.venv/bin/python \
  -r requirements.txt

/Users/Karthik/envs/datascience/.venv/bin/python download_sources.py
/Users/Karthik/envs/datascience/.venv/bin/python extract_august_2026.py
/Users/Karthik/envs/datascience/.venv/bin/python export_rajmargyatra_locations.py
/Users/Karthik/envs/datascience/.venv/bin/python analysis/summarise_august_2026.py
```

The download is roughly 80 MB. IHMCL can respond slowly, so downloads are
resumable and existing files are not fetched again.

## Repository policy

Raw PDFs, ZIP archives, API responses, extracted tables, checksums, and download
manifests are ignored. This repository is deliberately limited to code,
documentation, analysis, and findings.

IHMCL notes that reported ETC values may change after settlement and
reconciliation. Plaza-name matching also needs human review: IHMCL and
Rajmargyatra do not use one stable shared identifier in the published files.

## License

The code and original writing in this repository are available under the
[MIT License](LICENSE). Source data remains subject to the terms of its
respective publishers.
