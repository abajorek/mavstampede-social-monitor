"""Command line interface for the MavStampede Social Monitor."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd
import yaml

from src.classify.sentiment_rules import sentiment_from_score
from src.classify.themes import guess_themes
from src.filters.cmu_rules import score_text
from src.parsers.business_suite_csv_parser import normalize_df
from src.utils.io_utils import read_csvs

CONFIG_PATH = Path("config.yaml")
SCHEMA_COLUMNS = [
    "date_utc",
    "platform",
    "post_url",
    "post_owner_handle",
    "post_caption_excerpt",
    "comment_id",
    "commenter_handle",
    "comment_text",
    "sentiment",
    "themes",
    "confidence_cmumesa",
    "notes",
]


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Config file '{path}' is missing. Copy config.example.yaml to {path}"
        )
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    for column in SCHEMA_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[SCHEMA_COLUMNS]


def cmd_find(args: argparse.Namespace) -> None:
    config = load_config()
    keywords_path = Path(config["keywords_file"])
    keywords = [line.strip() for line in keywords_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({"query": keywords}).to_csv(output_path, index=False)
    print(f"Wrote candidate queries -> {output_path}")


def cmd_parse_exports(args: argparse.Namespace) -> None:
    source_dir = Path(args.in_dir)
    combined = read_csvs(source_dir)
    if combined.empty:
        print(f"No CSVs found in {source_dir}")
        raise SystemExit(1)

    normalized = normalize_df(combined)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(output_path, index=False)
    print(f"Normalized -> {output_path}")


def cmd_classify(args: argparse.Namespace) -> None:
    config = load_config()
    rules = config.get("rules", {})

    input_path = Path(args.in_)
    df = pd.read_csv(input_path)

    scores = df["comment_text"].fillna("").apply(lambda text: score_text(text, rules))
    df["sentiment"] = scores.apply(lambda item: sentiment_from_score(item.score))
    df["themes"] = df["comment_text"].fillna("").apply(lambda text: "|".join(guess_themes(text)))
    df["confidence_cmumesa"] = scores.apply(lambda item: item.confidence)
    df["notes"] = scores.apply(lambda item: item.notes)

    ordered = ensure_schema(df)

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ordered.to_csv(output_path, index=False)
    print(f"Classified -> {output_path}")


def cmd_export(args: argparse.Namespace) -> None:
    input_path = Path(args.in_)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_path, output_path)
    print(f"Exported -> {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    find_parser = subparsers.add_parser("find", help="Generate search queries")
    find_parser.set_defaults(func=cmd_find)
    find_parser.add_argument("--window", default="21d", help="Lookback window (unused placeholder)")
    find_parser.add_argument("--out", required=True, help="Output CSV path")

    parse_parser = subparsers.add_parser("parse-exports", help="Normalize CSV exports")
    parse_parser.set_defaults(func=cmd_parse_exports)
    parse_parser.add_argument("--in_dir", required=True, help="Directory containing CSV exports")
    parse_parser.add_argument("--out", required=True, help="Normalized CSV output path")

    classify_parser = subparsers.add_parser("classify", help="Classify normalized comments")
    classify_parser.set_defaults(func=cmd_classify)
    classify_parser.add_argument("--in", dest="in_", required=True, help="Input CSV path")
    classify_parser.add_argument("--out", required=True, help="Output CSV path")

    export_parser = subparsers.add_parser("export", help="Copy final CSV to destination")
    export_parser.set_defaults(func=cmd_export)
    export_parser.add_argument("--in", dest="in_", required=True, help="Input CSV path")
    export_parser.add_argument("--out", required=True, help="Output CSV path")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
