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

<!-- codex-session:01a110f1-29f1-71f3-9eb4-9896bbc7ae38:start -->
## 2026-10-06 16:50 IST | Codex session `01a110f1-29f`

### User prompts
> we have data from 2 data sources here right? what do they have, and cna they be joined?
> to start wtih, can we extract ALL the IHMCL data?
> dont' leave ambiguous duplicates in the data . will mess up downsteram analysis when done by a human. thisisa rule you should put in global agents.md andclaude.md

### Work done
- The repair code passed formatting and linting. A macOS multiprocessing limitation prevented the small one-off regeneration command from running when launched through stdin; the production script itself is unaffected....
- Fixed. - June Loni rows now resolve to: - 8,753 → Baghpat / Delhi - 3,383 → Aurangabad / Nagpur - All three canonical IHMCL tables now have zero duplicate plaza-month keys. - [extract_ihmcl.py](/Users/Karthik/Document...
- Touched files: `README.md`, `requirements.txt`, `analysis/explore_toll_plaza_data.Rmd`, `extract_ihmcl.py`
- README.md | 10 +++++++++-

<!-- codex-session:01a110f1-29f1-71f3-9eb4-9896bbc7ae38:end -->

<!-- codex-session:01a11192-fe75-7b13-9ec4-15d833f391bc:start -->
## 2026-10-06 19:46 IST | Codex session `01a11192-fe7`

### User prompts
> we have 2 datasets ehre. how do we merge theM/
> update that notebook to take into account all the data, now htat we hae some 5 years of data
> wby is this notebook abotu august only when we have such massive data ?

### Work done
- The August distribution and “busiest this month” sections are now removed. The main analysis uses every month: full-year indexed growth, all matched year-on-year plaza-months, four-year seasonality, entry cohorts, and...
- You were right—the previous revision still inherited the original August-map framing. That was my mistake. I’ve restructured [the notebook](/Users/Karthik/Documents/work/data_work/toll_plaza_map_data/analysis/explore_...
- Touched files: `README.md`, `requirements.txt`, `analysis/explore_toll_plaza_data.Rmd`, `extract_ihmcl.py`
- README.md | 10 +++++++++-

<!-- codex-session:01a11192-fe75-7b13-9ec4-15d833f391bc:end -->
