# MavStampede Social Monitor

MavStampede Social Monitor is a **CSV-first toolkit** for collecting, normalizing, and
classifying social media comments related to Colorado Mesa University's Maverick
Stampede marching band. The project avoids direct scraping by relying on CSV
exports that the user downloads manually from Facebook, Instagram, or TikTok.

The toolchain follows four primary steps:

1. **find** – produce keyword search queries to use when hunting for public posts.
2. **parse-exports** – load and normalize comment CSV exports from `data/raw/`.
3. **classify** – apply heuristic rules to assign CMU relevance, sentiment, and themes.
4. **export** – copy the classified data into the final reporting CSV.

## Quick start

These steps assume macOS/Linux with Python 3.11+ installed.  Windows users can
run the same commands inside PowerShell (replace the `source` line with
`.\.venv\Scripts\Activate.ps1`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp config.example.yaml config.yaml  # edit if you want to tweak rules/keywords

# Generate search ideas
python -m src.cli find --window 21d --out data/candidates.csv

# Drop your exported CSVs into data/raw/ then normalize + classify them
python -m src.cli parse-exports --in_dir data/raw --out data/comments_raw.csv
python -m src.cli classify --in data/comments_raw.csv --out data/comments_classified.csv

# Copy the classified data to the final report file
python -m src.cli export --in data/comments_classified.csv --out data/mavstampede_monitor.csv
```

Prefer a single command?  After installing the dependencies, drop at least one
export CSV into `data/raw/` and run:

```bash
make pipeline
```

This executes the same four CLI stages shown above (and will fail fast if no
CSV exports are present).  See [`Makefile`](Makefile) for additional helpers
like `make setup` and `make clean`.

## Web console

Prefer clicking?  The project ships with a lightweight Flask GUI that wraps the
same pipeline.  After installing the requirements, launch the console with:

```bash
export FLASK_APP=src.webapp:create_app
flask run --port 5001
```

Then open <http://127.0.0.1:5001/> to:

- Run the full pipeline or any individual stage with a single click.
- Preview the most recent `mavstampede_monitor.csv` output directly in the
  browser.
- Verify which pipeline artifacts exist and when they were last updated.

The console reads and writes the same files documented above, so you can mix
and match CLI + GUI runs without extra configuration.  Set `BOX_FIVE_DATA_DIR`
to point at an alternate data folder if desired, or `BOX_FIVE_SECRET_KEY` to
customize the session secret.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a deeper tour of the
stack, configuration, and development workflow.
