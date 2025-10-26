# Architecture Overview

## Stack
- **Python 3.11+** runtime
- **Pandas** for CSV handling
- **PyYAML** for configuration management
- **Playwright** (optional) helper scripts to open browser sessions that the user
  controls while gathering exports
- Lightweight modules under `src/` for parsing, scoring, and exporting data

## Key Modules
- `src/cli.py` – entrypoint with subcommands `find`, `parse-exports`, `classify`, `export`
- `src/utils/io_utils.py` – CSV loading helpers for `parse-exports`
- `src/parsers/business_suite_csv_parser.py` – normalizes Business Suite style CSV exports
- `src/filters/cmu_rules.py` – heuristic scoring for CMU relevance
- `src/classify/` – sentiment and theme helpers used during classification
- `src/export/to_csv.py` – basic CSV writer for final export step

## Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium  # optional, only if using the collectors

cp config.example.yaml config.yaml
python -m src.cli find --window 21d --out data/candidates.csv
python -m src.cli parse-exports --in_dir data/raw --out data/comments_raw.csv
python -m src.cli classify --in data/comments_raw.csv --out data/comments_classified.csv
python -m src.cli export --in data/comments_classified.csv --out data/mavstampede_monitor.csv
```

## Environment Variables
The CLI uses `config.yaml` for the small amount of configuration it needs. If you
want to manage settings through environment variables, consider creating an
`.env.example` mirroring the keys in `config.example.yaml` (time window, keyword
file, rules). For now, copying the example config is sufficient.

## Developer Commands
- `python -m src.cli ...` – run the CLI
- `pytest` – not yet configured, add tests as the project evolves
- `ruff`, `black`, `mypy` – recommended linting/type-checking tools (not bundled)

## Known Gaps / TODO
- [ ] Add automated tests for each CLI stage
- [ ] Support additional export formats beyond Facebook Business Suite
- [ ] Expand heuristics for sentiment and themes
- [ ] Provide richer logging and error handling across modules
- [ ] Flesh out Playwright collectors for Instagram and TikTok
