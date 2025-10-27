# Architecture Overview

## Stack
- **Python 3.11+** runtime
- **Pandas** for CSV handling
- **PyYAML** for configuration management
- **Playwright** (optional) helper scripts to open browser sessions that the user
  controls while gathering exports
- **Flask** web console under `src/webapp` to trigger the pipeline and preview data
- Lightweight modules under `src/` for parsing, scoring, and exporting data

## Key Modules
- `src/cli.py` – entrypoint with subcommands `find`, `parse-exports`, `classify`, `export`
- `src/utils/io_utils.py` – CSV loading helpers for `parse-exports`
- `src/parsers/business_suite_csv_parser.py` – normalizes Business Suite style CSV exports
- `src/filters/cmu_rules.py` – heuristic scoring for CMU relevance
- `src/classify/` – sentiment and theme helpers used during classification
- `src/export/to_csv.py` – basic CSV writer for final export step
- `src/webapp/` – Flask application with templates and static assets using CMU colors

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

# Optional Flask console
export FLASK_APP=src.webapp:create_app
flask run --port 5001
```

## Environment Variables
The CLI uses `config.yaml` for core settings. The web console also honors:

- `BOX_FIVE_DATA_DIR` – override the data directory (default `data/`)
- `BOX_FIVE_SECRET_KEY` – customize the Flask session secret

Consider adding an `.env` file with these values when deploying.

## Developer Commands
- `make setup` – create the virtualenv and install dependencies
- `make pipeline` – run the four CLI stages (find/parse/classify/export)
- `make gui` – start the Flask console on port 5001
- `python -m src.cli ...` – run an individual CLI command manually
- `pytest` – not yet configured, add tests as the project evolves
- `ruff`, `black`, `mypy` – recommended linting/type-checking tools (not bundled)

## Known Gaps / TODO
- [ ] Add automated tests for each CLI stage
- [ ] Support additional export formats beyond Facebook Business Suite
- [ ] Expand heuristics for sentiment and themes
- [ ] Provide richer logging and error handling across modules
- [ ] Flesh out Playwright collectors for Instagram and TikTok
- [ ] Add auth/session helpers for the Flask console
