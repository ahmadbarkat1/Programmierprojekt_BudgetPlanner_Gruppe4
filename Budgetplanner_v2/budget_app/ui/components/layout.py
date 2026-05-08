"""Shared layout helpers."""

from __future__ import annotations

from collections.abc import Callable

from nicegui import ui

from ...utils.date_utils import month_name, next_month, previous_month


def navigation(active_path: str) -> None:
    nav_items = [
        ("/", "home", "Übersicht"),
        ("/accounts", "account_balance_wallet", "Konten"),
        ("/categories", "sell", "Kategorien"),
        ("/budget", "inventory_2", "Budget"),
        ("/transactions", "sync_alt", "Transaktionen"),
    ]
    with ui.header(elevated=False).classes("bp-header"):
        with ui.row().classes("bp-shell w-full items-center justify-between py-4"):
            with ui.row().classes("items-center gap-3 no-wrap"):
                ui.icon("account_balance_wallet").classes("text-3xl text-teal-700")
                ui.label("Budget Planner").classes("text-2xl font-bold text-gray-900")
            ui.button("PDF Export", icon="picture_as_pdf", on_click=lambda: ui.run_javascript("window.print()")).classes("bp-secondary-btn")
    with ui.row().classes("bp-nav w-full"):
        with ui.row().classes("bp-shell w-full gap-8 overflow-x-auto no-wrap"):
            for path, icon, label in nav_items:
                classes = "bp-nav-link bp-nav-active" if active_path == path else "bp-nav-link"
                with ui.link(target=path).classes(classes):
                    with ui.row().classes("items-center gap-2 no-wrap"):
                        ui.icon(icon).classes("text-xl")
                        ui.label(label)


def page_container(active_path: str):
    navigation(active_path)
    return ui.column().classes("bp-page w-full gap-6")


def page_title(title: str, subtitle: str) -> None:
    with ui.column().classes("gap-1"):
        ui.label(title).classes("bp-title")
        ui.label(subtitle).classes("bp-muted")


def month_nav_card(path: str, year: int, month: int) -> None:
    previous_year, previous_month_value = previous_month(year, month)
    next_year, next_month_value = next_month(year, month)
    previous_target = f"{path}?year={previous_year}&month={previous_month_value}"
    next_target = f"{path}?year={next_year}&month={next_month_value}"
    with ui.card().classes("bp-card bp-month-card w-full p-5"):
        with ui.row().classes("w-full h-full items-center justify-between gap-3 no-wrap"):
            ui.button(icon="chevron_left", on_click=lambda: ui.navigate.to(previous_target)).props("flat round").classes("bp-month-arrow")
            with ui.column().classes("items-center gap-1"):
                ui.label("Monat").classes("text-sm bp-muted")
                ui.label(month_name(year, month)).classes("bp-month-value text-gray-900")
            ui.button(icon="chevron_right", on_click=lambda: ui.navigate.to(next_target)).props("flat round").classes("bp-month-arrow")


def empty_state(icon: str, title: str, description: str, cta: str | None = None, on_click: Callable[[], None] | None = None) -> None:
    with ui.element("div").classes("w-full p-10 text-center"):
        ui.icon(icon).classes("text-gray-300 text-6xl")
        ui.label(title).classes("text-lg font-semibold text-gray-800")
        ui.label(description).classes("bp-muted")
        if cta and on_click:
            ui.button(cta, on_click=on_click).classes("bp-primary-btn mt-3")
