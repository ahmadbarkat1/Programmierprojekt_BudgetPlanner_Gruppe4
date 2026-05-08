"""Date helpers used by UI and services."""

from __future__ import annotations

from datetime import date


MONTH_NAMES = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
]

MONTH_SHORT_NAMES = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]


def current_year_month() -> tuple[int, int]:
    """Return year and month from the system date."""
    today = date.today()
    return today.year, today.month


def month_name(year: int, month: int) -> str:
    return f"{MONTH_NAMES[month - 1]} {year}"


def month_short_label(year: int, month: int) -> str:
    return f"{MONTH_SHORT_NAMES[month - 1]} {str(year)[-2:]}"


def previous_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1
    return year, month + 1


def previous_months(year: int, month: int, count: int = 6) -> list[tuple[int, int]]:
    months: list[tuple[int, int]] = []
    cursor_year = year
    cursor_month = month
    for _ in range(count):
        months.append((cursor_year, cursor_month))
        cursor_year, cursor_month = previous_month(cursor_year, cursor_month)
    return list(reversed(months))


def add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(value.day, month_lengths[month - 1])
    return date(year, month, day)
