"""Bridge functions for calling CLI steps from the Flask console."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import Callable

from src import cli


def _ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def generate_candidates(out_path: Path, window: str = "21d") -> Path:
    """Run the CLI find step and return the generated CSV path."""
    out_path = _ensure_parent(out_path)
    cli.cmd_find(Namespace(out=str(out_path), window=window))
    return out_path


def normalize_exports(in_dir: Path, out_path: Path) -> Path:
    """Normalize CSV exports from the provided directory."""
    out_path = _ensure_parent(out_path)
    cli.cmd_parse_exports(Namespace(in_dir=str(in_dir), out=str(out_path)))
    return out_path


def classify_comments(in_path: Path, out_path: Path) -> Path:
    """Classify normalized comments using the configured rules."""
    out_path = _ensure_parent(out_path)
    cli.cmd_classify(Namespace(in_=str(in_path), out=str(out_path)))
    return out_path


def export_report(in_path: Path, out_path: Path) -> Path:
    """Copy the classified CSV into the final report location."""
    out_path = _ensure_parent(out_path)
    cli.cmd_export(Namespace(in_=str(in_path), out=str(out_path)))
    return out_path


def run_full_pipeline(
    raw_dir: Path,
    working_dir: Path,
    output_dir: Path,
    window: str = "21d",
    on_step: Callable[[str, Path], None] | None = None,
) -> Path:
    """Execute every stage of the pipeline and return the final CSV path."""
    candidates = generate_candidates(working_dir / "candidates.csv", window=window)
    if on_step:
        on_step("Candidates", candidates)

    normalized = normalize_exports(raw_dir, working_dir / "comments_raw.csv")
    if on_step:
        on_step("Normalized", normalized)

    classified = classify_comments(normalized, working_dir / "comments_classified.csv")
    if on_step:
        on_step("Classified", classified)

    final = export_report(classified, output_dir / "mavstampede_monitor.csv")
    if on_step:
        on_step("Exported", final)

    return final
