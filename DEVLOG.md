# Development log

## 6 October 2026 - session `initial-build`

### User prompts

> help me download the data used to prepare this map

> if you find the data sources, download as much data ase you can!

> make a git repo out ofit. public and MIT licensed. only code and repotts and analysis and insights. no data in the repo

### Work done

- Traced the map to IHMCL's August 2026 vehicle-class report and NHAI's
  Rajmargyatra plaza API.
- Downloaded and validated 56 months of vehicle-class reports plus related
  annual-pass, MLFF and location snapshots; kept the 79 MB archive outside Git.
- Extracted all 1,247 August rows and verified every reported total against the
  sum of its six vehicle classes.
- Added reproducible download, extraction and analysis scripts, initial
  findings, source caveats, an MIT license and strict data exclusions.
- Chose not to publish the original or derived data. The public repository holds
  only code and writing; users fetch source data from the publishers.
