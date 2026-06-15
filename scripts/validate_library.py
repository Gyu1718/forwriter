#!/usr/bin/env python3
"""Validate ForWriter Citation Library data files.

This is a lightweight validator using only Python standard library.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BOOKS_INDEX = DATA_DIR / "books_index.json"
BOOKS_DIR = DATA_DIR / "books"
QUOTES_DIR = DATA_DIR / "quotes"
TOPICS_DIR = DATA_DIR / "topics"

BOOK_ID_RE = re.compile(r"^[a-z0-9_]+$")
ALLOWED_BOOK_STATUS = {
    "not_started",
    "source_ready",
    "extracted",
    "summarized",
    "quote_candidates_ready",
    "reviewing",
    "verified",
    "needs_revision",
}
ALLOWED_QUOTE_CONFIDENCE = {"candidate", "needs_check", "verified", "rejected"}
ALLOWED_SOURCE_TYPES = {"pending", "epub", "pdf_text", "pdf_scan", "manual"}
ALLOWED_SOURCE_PREFIXES = ("private_sources/", "google_drive/private/")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise AssertionError(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc


def validate_book_record(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    if not isinstance(data, dict):
        return [f"{path.relative_to(ROOT)}: expected object"]

    book_id = data.get("book_id", "")
    if not book_id:
        errors.append(f"{path.relative_to(ROOT)}: missing book_id")
    elif not BOOK_ID_RE.match(book_id):
        errors.append(f"{path.relative_to(ROOT)}: invalid book_id: {book_id}")

    expected_name = f"{book_id}.json"
    if book_id and path.name != expected_name:
        errors.append(f"{path.relative_to(ROOT)}: filename should be {expected_name}")

    for required in ["title_ko", "author", "language", "source_type", "source_file", "status", "review_status"]:
        if required not in data:
            errors.append(f"{path.relative_to(ROOT)}: missing field {required}")

    if data.get("source_type") not in ALLOWED_SOURCE_TYPES:
        errors.append(f"{path.relative_to(ROOT)}: invalid source_type: {data.get('source_type')}")

    if data.get("status") not in ALLOWED_BOOK_STATUS:
        errors.append(f"{path.relative_to(ROOT)}: invalid status: {data.get('status')}")

    source_file = str(data.get("source_file", ""))
    if source_file and not source_file.startswith(ALLOWED_SOURCE_PREFIXES):
        errors.append(f"{path.relative_to(ROOT)}: source_file should point to private_sources/ or google_drive/private/")

    if not isinstance(data.get("chapter_summary", []), list):
        errors.append(f"{path.relative_to(ROOT)}: chapter_summary must be a list")
    if not isinstance(data.get("keywords", []), list):
        errors.append(f"{path.relative_to(ROOT)}: keywords must be a list")
    if not isinstance(data.get("themes", []), list):
        errors.append(f"{path.relative_to(ROOT)}: themes must be a list")
    if not isinstance(data.get("recommended_use", []), list):
        errors.append(f"{path.relative_to(ROOT)}: recommended_use must be a list")

    return errors


def validate_books_index(book_ids: set[str]) -> list[str]:
    errors: list[str] = []
    index = load_json(BOOKS_INDEX)
    if not isinstance(index, list):
        return ["data/books_index.json: expected array"]

    seen: set[str] = set()
    for idx, item in enumerate(index):
        prefix = f"data/books_index.json[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: expected object")
            continue
        book_id = item.get("book_id", "")
        if not book_id:
            errors.append(f"{prefix}: missing book_id")
        elif book_id not in book_ids:
            errors.append(f"{prefix}: book file missing for {book_id}")
        if book_id in seen:
            errors.append(f"{prefix}: duplicated book_id {book_id}")
        seen.add(book_id)

    missing_from_index = book_ids - seen
    for book_id in sorted(missing_from_index):
        errors.append(f"data/books_index.json: missing index entry for {book_id}")

    return errors


def validate_quote_file(path: Path, book_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen_quote_ids: set[str] = set()
    expected_book_id = path.name.removesuffix(".quotes.jsonl")

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        prefix = f"{path.relative_to(ROOT)}:{line_number}"
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{prefix}: invalid JSONL line: {exc}")
            continue

        quote_id = item.get("quote_id", "")
        book_id = item.get("book_id", "")
        quote = item.get("quote", "")
        confidence = item.get("confidence", "")

        if not quote_id:
            errors.append(f"{prefix}: missing quote_id")
        elif quote_id in seen_quote_ids:
            errors.append(f"{prefix}: duplicated quote_id {quote_id}")
        seen_quote_ids.add(quote_id)

        if book_id != expected_book_id:
            errors.append(f"{prefix}: book_id should match filename: {expected_book_id}")
        if book_id not in book_ids:
            errors.append(f"{prefix}: unknown book_id {book_id}")
        if not quote:
            errors.append(f"{prefix}: missing quote")
        if confidence not in ALLOWED_QUOTE_CONFIDENCE:
            errors.append(f"{prefix}: invalid confidence {confidence}")
        if not isinstance(item.get("theme", []), list):
            errors.append(f"{prefix}: theme must be a list")

    return errors


def main() -> None:
    errors: list[str] = []

    book_files = sorted(BOOKS_DIR.glob("*.json")) if BOOKS_DIR.exists() else []
    book_ids: set[str] = set()

    for path in book_files:
        data = load_json(path)
        if isinstance(data, dict) and data.get("book_id"):
            book_ids.add(str(data["book_id"]))
        errors.extend(validate_book_record(path))

    errors.extend(validate_books_index(book_ids))

    quote_files = sorted(QUOTES_DIR.glob("*.quotes.jsonl")) if QUOTES_DIR.exists() else []
    for path in quote_files:
        errors.extend(validate_quote_file(path, book_ids))

    if TOPICS_DIR.exists():
        for path in sorted(TOPICS_DIR.glob("*.json")):
            try:
                load_json(path)
            except AssertionError as exc:
                errors.append(str(exc))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Validation passed.")
    print(f"Books: {len(book_files)}")
    print(f"Quote files: {len(quote_files)}")


if __name__ == "__main__":
    main()
