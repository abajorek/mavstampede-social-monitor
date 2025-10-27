"""Flask web UI for the MavStampede Social Monitor."""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for

from src.cli import CONFIG_PATH, load_config
from . import pipeline

DEFAULT_WINDOW = "21d"


class WebConfig:
    """Simple container for filesystem paths used by the web UI."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.raw_dir = root / "raw"
        self.output_dir = root
        self.work_dir = root / "webapp"
        self.candidates_csv = root / "candidates.csv"
        self.normalized_csv = root / "comments_raw.csv"
        self.classified_csv = root / "comments_classified.csv"
        self.final_csv = root / "mavstampede_monitor.csv"

        self.root.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.work_dir.mkdir(parents=True, exist_ok=True)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("BOX_FIVE_SECRET_KEY", "development-secret")

    data_root = Path(os.environ.get("BOX_FIVE_DATA_DIR", "data")).resolve()
    app.config["WEB_CONFIG"] = WebConfig(data_root)

    @app.context_processor
    def inject_globals() -> dict:
        return {
            "config_path": CONFIG_PATH,
            "has_config": CONFIG_PATH.exists(),
        }

    @app.route("/", methods=["GET", "POST"])
    def index():
        web_config: WebConfig = app.config["WEB_CONFIG"]
        window = request.form.get("window", DEFAULT_WINDOW)
        if request.method == "POST":
            action = request.form.get("action")
            try:
                if action == "run_pipeline":
                    final_path = pipeline.run_full_pipeline(
                        raw_dir=web_config.raw_dir,
                        working_dir=web_config.work_dir,
                        output_dir=web_config.output_dir,
                        window=window,
                        on_step=lambda name, path: flash(
                            f"{name} ready → {path}", "info"
                        ),
                    )
                    flash(f"Pipeline complete → {final_path}", "success")
                elif action == "generate":
                    csv_path = pipeline.generate_candidates(web_config.candidates_csv, window)
                    flash(f"Generated search queries → {csv_path}", "success")
                elif action == "normalize":
                    csv_path = pipeline.normalize_exports(
                        web_config.raw_dir, web_config.normalized_csv
                    )
                    flash(f"Normalized exports → {csv_path}", "success")
                elif action == "classify":
                    csv_path = pipeline.classify_comments(
                        web_config.normalized_csv, web_config.classified_csv
                    )
                    flash(f"Classified comments → {csv_path}", "success")
                elif action == "export":
                    csv_path = pipeline.export_report(
                        web_config.classified_csv, web_config.final_csv
                    )
                    flash(f"Copied final report → {csv_path}", "success")
                else:
                    flash("Unknown action", "error")
            except FileNotFoundError as exc:
                flash(str(exc), "error")
            except SystemExit as exc:
                flash(f"Pipeline aborted: {exc}", "error")
            except Exception as exc:  # pylint: disable=broad-except
                flash(f"Unexpected error: {exc}", "error")

            return redirect(url_for("index"))

        final_preview = _load_preview(web_config.final_csv)
        status_cards = _build_status_cards(web_config)
        config_present = CONFIG_PATH.exists()
        try:
            rules = load_config() if config_present else {}
        except Exception as exc:  # pragma: no cover - surfaced in flash message already
            flash(f"Unable to load config: {exc}", "error")
            rules = {}

        return render_template(
            "index.html",
            window=window,
            status_cards=status_cards,
            final_preview=final_preview,
            rules=rules,
        )

    return app


def _load_preview(path: Path, limit: int = 25) -> pd.DataFrame | None:
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path).head(limit)
        return df
    except Exception:
        return None


def _build_status_cards(web_config: WebConfig) -> list[dict]:
    files = [
        ("Candidates", web_config.candidates_csv),
        ("Normalized", web_config.normalized_csv),
        ("Classified", web_config.classified_csv),
        ("Final Report", web_config.final_csv),
    ]
    status = []
    for label, path in files:
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            status.append({
                "label": label,
                "path": path,
                "exists": True,
                "mtime": mtime,
            })
        else:
            status.append({"label": label, "path": path, "exists": False, "mtime": None})
    return status
