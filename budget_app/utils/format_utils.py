"""Formatting and parsing helpers."""

from __future__ import annotations


def money(value: float) -> str:
    return f"CHF {value:,.2f}".replace(",", "’")


def parse_float(value: object, field_name: str) -> float:
    text = str(value or "").strip().replace("’", "").replace("'", "").replace(",", ".")
    if not text:
        raise ValueError(f"Bitte {field_name} erfassen.")
    return float(text)


def parse_int(value: object, field_name: str) -> int:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"Bitte {field_name} erfassen.")
    return int(text)
