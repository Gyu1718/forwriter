#!/usr/bin/env python3
"""Generate book records from data/intake/books_to_process.csv.

This script creates:
- data/books_index.json
- data/books/{book_id}.json

It does not read or upload EPUB/PDF source files.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTAKE_CSV = ROOT / "data" / "intake" / "books_to_process.csv"
BOOKS_DIR = ROOT / "data" / "books"
BOOKS_INDEX = ROOT / "data" / "books_index.json"

ALLOWED_SOURCE_TYPES = {"epub", "pdf_text", "pdf_scan", "manual"}
ALLOWED_PRIORITIES = {"high", "normal", "low", ""}
BOOK_ID_RE = re.compile(r"^[a-z0-9_]+$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clean(value: str | None) -> str:
    return (value or "").strip()


def split_list(value: str | None) -> list[str]:
    raw = clean(value)
    if not raw:
        return []
    return [part.strip() for part in raw.split(";") if part.strip()]


def validate_row(row: dict[str, str], row_number: int) -> list[str]:
    errors: list[str] = []

    book_id = clean(row.get("book_id"))
    title_ko = clean(row.get("title_ko"))
    author = clean(row.get("author"))
    language = clean(row.get("language"))
    source_type = clean(row.get("source_type"))
    source_file = clean(row.get("source_file"))
    priority = clean(row.get("priority"))

    if not book_id:
        errors.append(f"row {row_number}: book_id is required")
    elif not BOOK_ID_RE.match(book_id):
        errors.append(
            f"row {row_number}: book_id must use lowercase letters, numbers, and underscores only: {book_id!r}"
        )

    if not title_ko:
        errors.append(f"row {row_number}: title_ko is required")
    if not author:
        errors.append(f"row {row_number}: author is required")
    if not language:
        errors.append(f"row {row_number}: language is required")

    if source_type not in ALLOWED_SOURCE_TYPES:
        errors.append(
            f"row {row_number}: source_type must be one of {sorted(ALLOWED_SOURCE_TYPES)}: {source_type!r}"
        )

    if not source_file:
        errors.append(f"row {row_number}: source_file is required")
    elif not source_file.startswith("private_sources/"):
        errors.append(
            f"row {row_number}: source_file should point to private_sources/: {source_file!r}"
        )

    if priority not in ALLOWED_PRIORITIES:
        errors.append(
            f"row {row_number}: priority must be one of high, normal, low, or blank: {priority!r}"
        )

    return errors


def make_book_record(row: dict[str, str], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    existing = existing or {}
    timestamp = now_iso()

    book_id = clean(row.get("book_id"))
    title_ko = clean(row.get("title_ko"))
    title_original = clean(row.get("title_original"))
    author = clean(row.get("author"))

    return {
        "book_id": book_id,
        "title_ko": title_ko,
        "title_original": title_original,
        "author": author,
        "translator": clean(row.get("translator")),
        "publisher": clean(row.get("publisher")),
        "published_year": clean(row.get("published_year")),
        "edition": clean(row.get("edition")),
        "language": clean(row.get("language")),
        "source_type": clean(row.get("source_type")),
        "source_file": clean(row.get("source_file")),
        "isbn": clean(row.get("isbn")),
        "status": existing.get("status", "not_started"),
        "short_description": existing.get("short_description", ""),
        "detailed_description": existing.get("detailed_description", ""),
        "main_argument": existing.get("main_argument", ""),
        "chapter_summary": existing.get("chapter_summary", []),
        "keywords": existing.get("keywords", []),
        "themes": existing.get("themes", []),
        "recommended_use": existing.get("recommended_use", []),
        "review_status": existing.get("review_status", "needs_human_review"),
        "created_at": existing.get("created_at", timestamp),
        "updated_at": timestamp,
    }


def make_index_record(row: dict[str, str], book_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "book_id": book_record["book_id"],
        "title_ko": book_record["title_ko"],
        "title_original": book_record["title_original"],
        "author": book_record["author"],
        "source_type": book_record["source_type"],
        "source_available": False,
        "status": book_record["status"],
        "review_status": book_record["review_status"],
        "priority": clean(row.get("priority")) or "normal",
        "notes": clean(row.get("notes")),
    }


def read_existing_book(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid existing JSON file: {path}: {exc}") from exc


def main() -> None:
    if not INTAKE_CSV.exists():
        raise SystemExit(f"Missing intake CSV: {INTAKE_CSV}")

    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    with INTAKE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    errors: list[str] = []
    seen_ids: set[str] = set()

    for idx, row in enumerate(rows, start=2):
        row_errors = validate_row(row, idx)
        book_id = clean(row.get("book_id"))
        if book_id in seen_ids:
            row_errors.append(f"row {idx}: duplicated book_id: {book_id}")
        if book_id:
            seen_ids.add(book_id)
        errors.extend(row_errors)

    if errors:
        print("Input validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    index_records: list[dict[str, Any]] = []

    for row in rows:
        book_id = clean(row.get("book_id"))
        book_path = BOOKS_DIR / f"{book_id}.json"
        existing = read_existing_book(book_path)
        book_record = make_book_record(row, existing)
        index_records.append(make_index_record(row, book_record))
        book_path.write_text(
            json.dumps(book_record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {book_path.relative_to(ROOT)}")

    index_records.sort(key=lambda item: (item.get("priority") != "high", item["author"], item["title_ko"]))
    BOOKS_INDEX.write_text(
        json.dumps(index_records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {BOOKS_INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
