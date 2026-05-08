"""Reusable card components."""

from __future__ import annotations

from nicegui import ui

from ...services.budget_service import BudgetStatus
from ...utils.format_utils import money


def stat_card(title: str, value: str, icon: str, tone: str, subtitle: str | None = None) -> None:
    tones = {
        "green": ("bg-green-100", "text-green-700", "bp-positive"),
        "red": ("bg-red-100", "text-red-700", "bp-negative"),
        "blue": ("bg-blue-100", "text-blue-700", "bp-blue"),
        "amber": ("bg-amber-100", "text-amber-700", "bp-warning"),
        "neutral": ("bg-gray-100", "text-gray-700", "text-gray-900"),
    }
    bg_class, icon_class, value_class = tones[tone]
    with ui.card().classes("bp-card bp-stat-card w-full p-6"):
        with ui.row().classes("w-full items-start justify-between gap-4 no-wrap"):
            with ui.column().classes("gap-2"):
                ui.label(title).classes("text-sm bp-muted")
                ui.label(value).classes(f"bp-stat-value text-2xl font-bold {value_class}")
                if subtitle:
                    ui.label(subtitle).classes("text-xs bp-muted")
            with ui.element("div").classes(f"{bg_class} rounded-full w-11 h-11 flex items-center justify-center"):
                ui.icon(icon).classes(f"text-xl {icon_class}")


def progress_bar(percent: float, tone: str) -> None:
    width = max(0, min(percent, 100))
    fill_class = {
        "ok": "bp-progress-ok",
        "warning": "bp-progress-warning",
        "danger": "bp-progress-danger",
    }[tone]
    with ui.element("div").classes("bp-progress"):
        ui.element("div").classes(f"bp-progress-fill {fill_class}").style(f"width: {width:.1f}%")


def budget_tone(percent: float, remaining_chf: float) -> str:
    if remaining_chf < 0 or percent > 100:
        return "danger"
    if percent >= 80:
        return "warning"
    return "ok"


def envelope_card(status: BudgetStatus) -> None:
    budget = status.budget
    percent = (status.spent_chf / budget.limit_chf * 100) if budget.limit_chf else 0
    tone = budget_tone(percent, status.remaining_chf)
    envelope_class = {
        "ok": "bp-envelope-ok",
        "warning": "bp-envelope-warning",
        "danger": "bp-envelope-danger",
    }[tone]
    status_class = {"ok": "bp-positive", "warning": "bp-warning", "danger": "bp-negative"}[tone]
    with ui.card().classes(f"bp-card bp-envelope-card {envelope_class} bp-card-hover w-full p-4"):
        with ui.row().classes("w-full items-start justify-between gap-3 no-wrap"):
            with ui.column().classes("gap-1"):
                ui.label(budget.category.name).classes("text-lg font-bold text-gray-900")
                ui.label(f"{budget.month:02d}.{budget.year}").classes("text-xs bp-muted")
            ui.label(f"{percent:.0f}%").classes(f"text-xl font-bold {status_class}")
        with ui.column().classes("gap-3 mt-3"):
            with ui.row().classes("w-full justify-between"):
                ui.label("Verbraucht").classes("text-sm bp-muted")
                ui.label(f"{money(status.spent_chf)} von {money(budget.limit_chf)}").classes("text-sm bp-muted")
            progress_bar(percent, tone)
            with ui.element("div").classes("bp-compact-metrics"):
                with ui.column().classes("bp-metric-box gap-0"):
                    ui.label("Budget").classes("text-xs bp-muted")
                    ui.label(money(budget.limit_chf)).classes("font-semibold bp-money")
                with ui.column().classes("bp-metric-box gap-0"):
                    ui.label("Verbrauch").classes("text-xs bp-muted")
                    ui.label(money(status.spent_chf)).classes("font-semibold bp-money")
                with ui.column().classes("bp-metric-box gap-0"):
                    ui.label("Rest").classes("text-xs bp-muted")
                    ui.label(money(status.remaining_chf)).classes(f"font-semibold bp-money {status_class}")
