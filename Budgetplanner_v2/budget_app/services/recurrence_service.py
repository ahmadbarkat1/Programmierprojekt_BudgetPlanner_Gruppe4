"""Recurrence strategies for repeated transactions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, timedelta

from ..utils.date_utils import add_months


class RecurrenceStrategy(ABC):
    """Strategy interface for calculating future transaction dates."""

    @abstractmethod
    def next_date(self, current: date) -> date:
        raise NotImplementedError


class WeeklyRecurrenceStrategy(RecurrenceStrategy):
    def next_date(self, current: date) -> date:
        return current + timedelta(days=7)


class MonthlyRecurrenceStrategy(RecurrenceStrategy):
    def next_date(self, current: date) -> date:
        return add_months(current, 1)


class QuarterlyRecurrenceStrategy(RecurrenceStrategy):
    def next_date(self, current: date) -> date:
        return add_months(current, 3)


class YearlyRecurrenceStrategy(RecurrenceStrategy):
    def next_date(self, current: date) -> date:
        return add_months(current, 12)


class RecurrenceService:
    """Facade over recurrence strategies."""

    _strategies: dict[str, RecurrenceStrategy] = {
        "weekly": WeeklyRecurrenceStrategy(),
        "monthly": MonthlyRecurrenceStrategy(),
        "quarterly": QuarterlyRecurrenceStrategy(),
        "yearly": YearlyRecurrenceStrategy(),
    }

    @classmethod
    def dates(cls, start_date: date, frequency: str, occurrences: int) -> list[date]:
        if occurrences < 1:
            raise ValueError("Anzahl Wiederholungen muss mindestens 1 sein.")
        strategy = cls._strategies.get(frequency)
        if strategy is None:
            raise ValueError("Unbekannte Wiederholung.")
        dates = [start_date]
        current = start_date
        for _ in range(occurrences - 1):
            current = strategy.next_date(current)
            dates.append(current)
        return dates
