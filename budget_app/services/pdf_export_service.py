"""Structured PDF export for the Budget Planner."""

from __future__ import annotations

from calendar import monthrange
from collections import defaultdict
from io import BytesIO
from math import cos, pi, sin
from typing import TYPE_CHECKING

from ..utils.date_utils import month_name, month_short_label, previous_month, previous_months

if TYPE_CHECKING:
    from ..ui.controllers import FinanceController


PAGE_WIDTH = 842
PAGE_HEIGHT = 595
MARGIN = 8
CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2

COLORS = {
    "page": "#f8fafc",
    "card": "#ffffff",
    "border": "#dbe3ef",
    "text": "#111827",
    "muted": "#64748b",
    "header": "#111827",
    "blue": "#2563eb",
    "green": "#16a34a",
    "red": "#dc2626",
    "amber": "#f59e0b",
    "teal": "#0f766e",
    "soft_green": "#c7f2e7",
    "soft_blue": "#e6edf7",
    "soft_pink": "#ffd4de",
}

AREA_ORDER = ["overview", "accounts", "categories", "budgets", "transactions"]


def export_budgetplanner_pdf(controller: "FinanceController", areas: list[str], year: int, month: int) -> bytes:
    """Create a compact A4 portrait PDF with at most one page per selected area."""
    selected = [area for area in AREA_ORDER if area in areas]
    pages = []
    for area in selected:
        show_document_title = not pages
        if area == "overview":
            pages.append(_overview_page(controller, year, month, show_document_title))
        if area == "accounts":
            pages.append(_accounts_page(controller, year, month, show_document_title))
        if area == "categories":
            pages.append(_categories_page(controller, year, month, show_document_title))
        if area == "budgets":
            pages.append(_budgets_page(controller, year, month, show_document_title))
        if area == "transactions":
            pages.append(_transactions_page(controller, year, month, show_document_title))
    return _build_pdf(pages)


def _base_page(section_title: str, year: int, month: int, show_document_title: bool) -> list[str]:
    commands = [_rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, COLORS["page"])]
    _page_wash(commands)
    commands.append(_text(MARGIN, PAGE_HEIGHT - 26, section_title, 17, True, COLORS["text"]))
    subtitle = {
        "Übersicht": "Dein Budgetstatus für den aktuellen Monat auf einen Blick.",
        "Konten": "Verwalte Bankkonto und Bargeld mit klarem aktuellem Saldo.",
        "Kategorien": "Ordne Einnahmen und Ausgaben sauber deinen Budgets zu.",
        "Budget": "Plane dein Monatsbudget nach Kategorie und sieh sofort, wo du noch Luft hast.",
        "Transaktionen": "Erfasse Einnahmen und Ausgaben mit passenden Kategorien und Konten.",
    }.get(section_title, "")
    if subtitle:
        commands.append(_text(MARGIN, PAGE_HEIGHT - 45, subtitle, 8.6, False, COLORS["muted"]))
    return commands


def _content_top(show_document_title: bool) -> float:
    return 545


def _overview_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> bytes:
    data = controller.dashboard_data(year=year, month=month)
    all_transactions = controller.list_recent_transactions()
    accounts = controller.list_accounts()
    total_account_balance = sum(_account_balance(account, all_transactions) for account in accounts)
    total_budget = sum(status.budget.limit_chf for status in data.budget_statuses)
    budgeted_category_ids = {status.budget.category_id for status in data.budget_statuses}
    budgeted_expenses = sum(
        transaction.amount_chf
        for transaction in data.transactions
        if transaction.transaction_type == "expense" and transaction.category_id in budgeted_category_ids
    )
    remaining = total_budget - budgeted_expenses

    commands = _base_page("Übersicht", year, month, show_document_title)
    top = _content_top(show_document_title)
    _metric_cards(
        commands,
        [
            ("Noch verfügbar", _money(remaining), COLORS["green"] if remaining >= 0 else COLORS["red"]),
            ("Einnahmen", _money(data.overview.total_income_chf), COLORS["green"]),
            ("Ausgaben", _money(data.overview.total_expenses_chf), COLORS["red"]),
        ],
        top,
        month_name(year, month),
    )

    category_totals: dict[str, float] = defaultdict(float)
    for transaction in data.transactions:
        if transaction.transaction_type == "expense":
            category_totals[transaction.category.name] += transaction.amount_chf
    monthly = []
    for comparison_year, comparison_month in previous_months(year, month):
        month_data = controller.dashboard_data(year=comparison_year, month=comparison_month)
        monthly.append(
            {
                "month": month_short_label(comparison_year, comparison_month),
                "income": month_data.overview.total_income_chf,
                "expenses": month_data.overview.total_expenses_chf,
            }
        )
    average, current = _expense_progress_series(controller, year, month)

    _category_chart(commands, 8, 240, 410, 230, category_totals)
    _monthly_chart(commands, 426, 240, 408, 230, monthly)
    _progress_chart(commands, 8, 18, 684, 205, average, current)
    return _stream(commands)


def _accounts_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> bytes:
    commands = _base_page("Konten", year, month, show_document_title)
    accounts = controller.list_accounts()
    transactions = controller.list_recent_transactions()
    total_start = sum(account.starting_balance_chf for account in accounts)
    total_balance = sum(_account_balance(account, transactions) for account in accounts)
    top = _content_top(show_document_title)
    commands.append(_text(12, top - 34, "Gesamtübersicht", 10.5, True, COLORS["text"]))
    panel_y = top - 142
    _card(commands, 3, panel_y, 836, 100)
    commands.append(_rect(12, panel_y + 18, 280, 64, COLORS["header"]))
    commands.append(_text(24, panel_y + 60, "Aktueller Gesamtsaldo", 6.8, False, "#ffffff"))
    commands.append(_text(24, panel_y + 34, _money(total_balance), 17, True, "#ffffff"))
    commands.append(_text(24, panel_y + 14, f"{len(accounts)} Konten aktiv", 9.2, False, "#ffffff"))
    _mini_summary(commands, 300, panel_y + 18, 262, 64, "Anzahl Konten", str(len(accounts)))
    _mini_summary(commands, 570, panel_y + 18, 260, 64, "Gesamter Startsaldo", _money(total_start))

    card_w = 274
    card_h = 150
    gap = 10
    start_y = panel_y - 165
    for index, account in enumerate(accounts[:6]):
        col = index % 3
        row = index // 3
        x = 3 + col * (card_w + gap)
        y = start_y - row * (card_h + 12)
        _account_card(commands, x, y, card_w, card_h, account, transactions)
    return _stream(commands)


def _categories_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> bytes:
    commands = _base_page("Kategorien", year, month, show_document_title)
    transactions = controller.list_recent_transactions()
    rows = [
        [
            category.name,
            "Einnahme" if category.category_type == "income" else "Ausgabe",
            str(sum(1 for transaction in transactions if transaction.category_id == category.id)),
        ]
        for category in controller.list_categories()
    ]
    _table(commands, 8, 22, 640, 500, ["Kategoriename", "Typ", "Verwendungen"], rows, pill_column=1)
    return _stream(commands)


def _budgets_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> bytes:
    data = controller.dashboard_data(year=year, month=month)
    budgets = controller.list_budgets(year=year, month=month)
    budget_limit = sum(budget.limit_chf for budget in budgets)
    expenses = sum(transaction.amount_chf for transaction in data.transactions if transaction.transaction_type == "expense")
    remaining = budget_limit - expenses
    usage = expenses / budget_limit * 100 if budget_limit else 0

    commands = _base_page("Budget", year, month, show_document_title)
    top = _content_top(show_document_title)
    _metric_cards(
        commands,
        [
            ("Budget", _money(budget_limit), COLORS["blue"]),
            ("Ausgaben", _money(expenses), COLORS["red"]),
            ("Verbleibend", _money(remaining), COLORS["green"] if remaining >= 0 else COLORS["red"]),
            ("Auslastung", f"{usage:.0f}%", COLORS["amber"] if usage >= 80 else COLORS["teal"]),
        ],
        top,
        month_name(year, month),
    )
    commands.append(_text(8, 388, "Budgets für diesen Monat", 12, True, COLORS["text"]))
    _budget_total_card(commands, 8, 228, 154, 130, remaining, expenses, budget_limit)
    card_w = 154
    card_h = 130
    for index, status in enumerate(data.budget_statuses[:9]):
        if index < 4:
            x = 170 + index * (card_w + 8)
            y = 228
        else:
            x = 8 + (index - 4) * (card_w + 8)
            y = 80
        _budget_card(commands, x, y, card_w, card_h, status)
    return _stream(commands)


def _transactions_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> bytes:
    commands = _base_page("Transaktionen", year, month, show_document_title)
    user = controller.default_user()
    transactions = sorted(
        controller.transaction_service.list_for_month(year=year, month=month, user_id=user.id),
        key=lambda item: (item.transaction_date, item.id or 0),
        reverse=True,
    )
    max_rows = 28
    visible = transactions[:max_rows]
    rows = []
    for transaction in visible:
        is_income = transaction.transaction_type == "income"
        amount = transaction.amount_chf if is_income else -transaction.amount_chf
        rows.append(
            [
                transaction.transaction_date.strftime("%d.%m.%Y"),
                "Einnahme" if is_income else "Ausgabe",
                transaction.category.name,
                transaction.account.name,
                transaction.description or "-",
                _money(amount),
            ]
        )
    commands.append(_text(8, 492, month_name(year, month), 9.5, True, COLORS["text"]))
    _table(commands, 6, 22, 830, 450, ["Datum", "Typ", "Kategorie", "Konto", "Beschreibung", "Betrag"], rows, color_column=5, pill_column=1)
    if len(transactions) > max_rows:
        commands.append(_text(40, 102, "Weitere Transaktionen sind in der App sichtbar.", 8, False, COLORS["muted"]))
    return _stream(commands)


def _metric_cards(commands: list[str], cards: list[tuple[str, str, str]], y: float, subtitle: str = "") -> None:
    gap = 10
    width = (CONTENT_WIDTH - gap * (len(cards) - 1)) / len(cards)
    for index, (label, value, color) in enumerate(cards):
        x = MARGIN + index * (width + gap)
        _card(commands, x, y - 64, width, 64)
        commands.append(_text(x + 12, y - 22, label, 7.2, False, COLORS["muted"]))
        commands.append(_text(x + 12, y - 44, _clip(value, 22), 14, True, color))
        if subtitle:
            commands.append(_text(x + 12, y - 58, subtitle, 6.2, False, COLORS["muted"]))


def _mini_summary(commands: list[str], x: float, y: float, width: float, height: float, label: str, value: str) -> None:
    commands.append(_rect(x, y, width, height, "#f8fafc"))
    commands.append(_stroke_rect(x, y, width, height, "#e5e7eb", 0.5))
    commands.append(_text(x + 10, y + height - 22, label, 8.2, False, COLORS["muted"]))
    commands.append(_text(x + 10, y + 21, value, 11, True, COLORS["text"]))


def _account_card(commands: list[str], x: float, y: float, width: float, height: float, account, transactions) -> None:
    balance = _account_balance(account, transactions)
    tx_count = sum(1 for transaction in transactions if transaction.account_id == account.id)
    tone = COLORS["green"] if balance >= 0 else COLORS["red"]
    _card(commands, x, y, width, height)
    icon_color = "#dbeafe" if account.account_type == "Bankkonto" else "#fef3c7"
    commands.append(_rect(x + 14, y + height - 38, 24, 24, icon_color))
    commands.append(_text(x + 50, y + height - 22, _clip(account.name, 24), 9, True, COLORS["text"]))
    commands.append(_pill(x + 50, y + height - 40, account.account_type, COLORS["blue"] if account.account_type == "Bankkonto" else "#92400e"))
    commands.append(_text(x + 14, y + height - 72, "Aktueller Saldo", 5.8, False, COLORS["muted"]))
    commands.append(_text(x + 14, y + height - 96, _money(balance), 13, True, tone))
    commands.append(_line([(x + 14, y + 52), (x + width - 14, y + 52)], "#d1d5db", 0.45))
    commands.append(_text(x + 14, y + 32, "Startsaldo", 8, False, COLORS["muted"]))
    commands.append(_text(x + width - 74, y + 32, _money(account.starting_balance_chf), 8, True, COLORS["text"]))
    commands.append(_text(x + 14, y + 14, "Transaktionen", 8, False, COLORS["muted"]))
    commands.append(_text(x + width - 24, y + 14, str(tx_count), 8, True, COLORS["text"]))


def _budget_total_card(commands: list[str], x: float, y: float, width: float, height: float, remaining: float, expenses: float, limit: float) -> None:
    usage = expenses / limit * 100 if limit else 0
    commands.append(_rect(x, y, width, height, COLORS["header"]))
    commands.append(_text(x + 10, y + height - 20, "Alle Budgets", 6.5, False, "#ffffff"))
    commands.append(_text(x + 10, y + height - 42, _money(remaining), 14, True, "#ffffff"))
    commands.append(_text(x + 10, y + height - 58, f"{_money(expenses)} von {_money(limit)}", 6.2, False, "#ffffff"))
    commands.append(_rect(x + 10, y + 14, width - 20, 5, "#dbe3ef"))
    commands.append(_rect(x + 10, y + 14, (width - 20) * min(max(usage, 0), 100) / 100, 5, COLORS["green"] if remaining >= 0 else COLORS["red"]))


def _budget_card(commands: list[str], x: float, y: float, width: float, height: float, status) -> None:
    limit = status.budget.limit_chf
    percent = status.spent_chf / limit * 100 if limit else 0
    tone = COLORS["red"] if status.remaining_chf < 0 else COLORS["amber"] if percent >= 80 else COLORS["green"]
    _card(commands, x, y, width, height)
    commands.append(_line([(x, y), (x, y + height)], tone, 2.2))
    commands.append(_text(x + 12, y + height - 22, _clip(status.budget.category.name, 16), 10, True, COLORS["text"]))
    commands.append(_text(x + width - 50, y + height - 22, f"{percent:.0f}%", 10, True, tone))
    commands.append(_rect(x + 12, y + height - 70, width - 24, 6, "#e5e7eb"))
    commands.append(_rect(x + 12, y + height - 70, (width - 24) * min(max(percent, 0), 100) / 100, 6, tone))
    third = (width - 22) / 3
    for index, (label, value, color) in enumerate(
        [
            ("Budget", _money(limit, decimals=0), COLORS["text"]),
            ("Verbrauch", _money(status.spent_chf, decimals=0), COLORS["text"]),
            ("Rest", _money(status.remaining_chf, decimals=0), tone),
        ]
    ):
        box_x = x + 8 + index * (third + 3)
        commands.append(_rect(box_x, y + 16, third, 34, "#f8fafc"))
        commands.append(_stroke_rect(box_x, y + 16, third, 34, "#e5e7eb", 0.35))
        commands.append(_text(box_x + 5, y + 38, label, 5.8, False, COLORS["muted"]))
        commands.append(_text(box_x + 5, y + 24, value, 7.1, True, color))


def _category_chart(commands: list[str], x: float, y: float, width: float, height: float, totals: dict[str, float]) -> None:
    _panel(commands, x, y, width, height, "Ausgaben nach Kategorie")
    items = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:7]
    if not items:
        commands.append(_text(x + 14, y + height / 2, "Keine Ausgaben vorhanden.", 8, False, COLORS["muted"]))
        return
    total = sum(value for _, value in items) or 1
    palette = ["#5470c6", "#b6dc29", "#fb923c", "#0ea5e9", "#facc15", "#f06292", "#7e65b8"]
    cx = x + 76
    cy = y + 92
    radius = 52
    start_angle = -pi / 2
    for index, (_, value) in enumerate(items):
        end_angle = start_angle + 2 * pi * value / total
        _donut_slice(commands, cx, cy, radius, 28, start_angle, end_angle, palette[index % len(palette)])
        start_angle = end_angle
    commands.append(_text(cx - 17, cy - 3, "CHF", 7, True, COLORS["muted"]))
    legend_x = x + 150
    for index, (name, value) in enumerate(items):
        row_y = y + height - 50 - index * 17
        commands.append(_rect(legend_x, row_y, 7, 7, palette[index % len(palette)]))
        commands.append(_text(legend_x + 11, row_y - 1, _clip(name, 13), 6.7, False, COLORS["muted"]))


def _monthly_chart(commands: list[str], x: float, y: float, width: float, height: float, values: list[dict[str, float | str]]) -> None:
    _panel(commands, x, y, width, height, "Einnahmen vs. Ausgaben")
    if not values:
        commands.append(_text(x + 14, y + height / 2, "Keine Monatsdaten vorhanden.", 8, False, COLORS["muted"]))
        return
    chart_x = x + 38
    chart_y = y + 34
    chart_h = height - 76
    chart_w = width - 58
    max_value = max(max(float(item["income"]), float(item["expenses"])) for item in values) or 1
    _grid(commands, chart_x, chart_y, chart_w, chart_h, max_value)
    group = chart_w / len(values)
    bar_w = min(12, group * 0.22)
    for index, item in enumerate(values):
        center = chart_x + index * group + group / 2
        income_h = chart_h * float(item["income"]) / max_value
        expense_h = chart_h * float(item["expenses"]) / max_value
        commands.append(_rect(center - bar_w - 2, chart_y, bar_w, income_h, COLORS["green"]))
        commands.append(_rect(center + 2, chart_y, bar_w, expense_h, COLORS["red"]))
        commands.append(_text(center - 14, chart_y - 14, str(item["month"]), 6.5, False, COLORS["muted"]))
    _legend(commands, x + 48, y + height - 33, [("Einnahmen", COLORS["green"]), ("Ausgaben", COLORS["red"])])


def _progress_chart(commands: list[str], x: float, y: float, width: float, height: float, average: list[float], current: list[float | None]) -> None:
    _panel(commands, x, y, width, height, "Ausgabenverlauf")
    chart_x = x + 44
    chart_y = y + 36
    chart_w = width - 72
    chart_h = height - 82
    values = average + [value for value in current if value is not None]
    max_value = max(values) if values else 1
    _grid(commands, chart_x, chart_y, chart_w, chart_h, max_value)
    commands.append(_line(_line_points(average, chart_x, chart_y, chart_w, chart_h, max_value), COLORS["muted"], 1.6))
    commands.append(_line(_line_points(current, chart_x, chart_y, chart_w, chart_h, max_value), COLORS["blue"], 1.9))
    commands.append(_text(chart_x + chart_w / 2 - 28, chart_y - 22, "Tage im Monat", 7, True, COLORS["muted"]))
    commands.append(_text(x + 12, chart_y + chart_h / 2, "Ausgabe (CHF)", 7, True, COLORS["muted"]))
    _legend(commands, x + 48, y + height - 34, [("Durchschnitt letzte 3 Monate", COLORS["muted"]), ("Aktueller Monat", COLORS["blue"])])


def _table(
    commands: list[str],
    x: float,
    y: float,
    width: float,
    height: float,
    headers: list[str],
    rows: list[list[str]],
    align_right: set[int] | None = None,
    color_column: int | None = None,
    pill_column: int | None = None,
) -> None:
    align_right = align_right or set()
    columns = _column_widths(headers)
    row_count = max(1, len(rows))
    row_h = min(19, max(12, (height - 30) / (row_count + 1)))
    font_size = min(8.2, max(6.0, row_h - 5))
    max_rows = int((height - 30) // row_h) - 1
    visible_rows = rows[:max_rows]
    _card(commands, x, y, width, height)
    commands.append(_rect(x, y + height - 26, width, 26, "#eef2f7"))
    cursor = x + 8
    for index, header in enumerate(headers):
        col_w = width * columns[index]
        commands.append(_text(cursor, y + height - 17, header, 7.4, True, COLORS["muted"]))
        cursor += col_w
    line_y = y + height - 26 - row_h
    for row in visible_rows:
        commands.append(_line([(x + 8, line_y + row_h - 3), (x + width - 8, line_y + row_h - 3)], "#e5e7eb", 0.45))
        cursor = x + 8
        for index, value in enumerate(row):
            col_w = width * columns[index]
            color = COLORS["text"]
            if color_column == index:
                color = COLORS["red"] if str(value).strip().startswith("-") else COLORS["green"]
            text_x = cursor if index not in align_right else cursor + col_w - 8 - _estimated_text_width(str(value), font_size)
            if pill_column == index:
                pill_color = COLORS["green"] if str(value) == "Einnahme" else COLORS["red"]
                commands.append(_pill(text_x, line_y + 3, str(value), pill_color))
            else:
                commands.append(_text(text_x, line_y + 5, _clip(str(value), max(8, int(col_w / (font_size * 0.48)))), font_size, False, color))
            cursor += col_w
        line_y -= row_h
    if len(rows) > len(visible_rows):
        commands.append(_text(x + 8, y + 10, "Weitere Einträge sind in der App sichtbar.", 7, False, COLORS["muted"]))


def _column_widths(headers: list[str]) -> list[float]:
    presets = {
        3: [0.48, 0.31, 0.21],
        4: [0.34, 0.22, 0.22, 0.22],
        5: [0.33, 0.17, 0.18, 0.17, 0.15],
        6: [0.14, 0.13, 0.18, 0.16, 0.27, 0.12],
    }
    return presets.get(len(headers), [1 / len(headers)] * len(headers))


def _expense_progress_series(controller: "FinanceController", year: int, month: int) -> tuple[list[float], list[float | None]]:
    comparison_months = []
    cursor_year, cursor_month = year, month
    for _ in range(3):
        cursor_year, cursor_month = previous_month(cursor_year, cursor_month)
        comparison_months.append((cursor_year, cursor_month))
    comparison_months.reverse()
    day_count = monthrange(year, month)[1]
    days = list(range(1, day_count + 1))
    previous_values = []
    for comparison_year, comparison_month in comparison_months:
        month_data = controller.dashboard_data(year=comparison_year, month=comparison_month)
        by_day: dict[int, float] = defaultdict(float)
        for transaction in month_data.transactions:
            if transaction.transaction_type == "expense":
                by_day[transaction.transaction_date.day] += transaction.amount_chf
        running = 0.0
        values = []
        comparison_days = monthrange(comparison_year, comparison_month)[1]
        for day in days:
            if day <= comparison_days:
                running += by_day.get(day, 0.0)
            values.append(running)
        previous_values.append(values)
    average = [sum(month_values[index] for month_values in previous_values) / len(previous_values) for index in range(day_count)]
    current_data = controller.dashboard_data(year=year, month=month)
    by_day: dict[int, float] = defaultdict(float)
    max_day = 0
    for transaction in current_data.transactions:
        if transaction.transaction_type == "expense":
            by_day[transaction.transaction_date.day] += transaction.amount_chf
            max_day = max(max_day, transaction.transaction_date.day)
    running = 0.0
    current = []
    for day in days:
        if max_day and day <= max_day:
            running += by_day.get(day, 0.0)
            current.append(running)
        else:
            current.append(None)
    return average, current


def _account_balance(account, transactions) -> float:
    balance = account.starting_balance_chf
    for transaction in transactions:
        if transaction.account_id == account.id:
            balance += transaction.amount_chf if transaction.transaction_type == "income" else -transaction.amount_chf
    return round(balance, 2)


def _panel(commands: list[str], x: float, y: float, width: float, height: float, title: str) -> None:
    _card(commands, x, y, width, height)
    commands.append(_text(x + 12, y + height - 20, title, 9.3, True, COLORS["text"]))


def _page_wash(commands: list[str]) -> None:
    commands.append(_rect(0, PAGE_HEIGHT - 58, PAGE_WIDTH * 0.34, 58, COLORS["soft_green"]))
    commands.append(_rect(PAGE_WIDTH * 0.34, PAGE_HEIGHT - 58, PAGE_WIDTH * 0.36, 58, COLORS["soft_blue"]))
    commands.append(_rect(PAGE_WIDTH * 0.70, PAGE_HEIGHT - 58, PAGE_WIDTH * 0.30, 58, COLORS["soft_pink"]))


def _card(commands: list[str], x: float, y: float, width: float, height: float) -> None:
    commands.append(_rect(x, y, width, height, COLORS["card"]))
    commands.append(_stroke_rect(x, y, width, height, COLORS["border"], 0.7))


def _pill(x: float, y: float, text: str, color: str) -> str:
    bg = "#dcfce7" if color == COLORS["green"] else "#fee2e2" if color == COLORS["red"] else "#dbeafe" if color == COLORS["blue"] else "#fef3c7"
    width = max(34, _estimated_text_width(text, 6.5) + 13)
    return "\n".join(
        [
            _rect(x, y, width, 13, bg),
            _text(x + 5, y + 4, text, 6.5, True, color),
        ]
    )


def _grid(commands: list[str], x: float, y: float, width: float, height: float, max_value: float) -> None:
    commands.append(_line([(x, y), (x + width, y)], "#cbd5e1", 0.5))
    for index in range(1, 4):
        grid_y = y + height * index / 4
        commands.append(_line([(x, grid_y), (x + width, grid_y)], "#e5e7eb", 0.35))
        commands.append(_text(x - 30, grid_y - 2, _compact(max_value * index / 4), 5.7, False, COLORS["muted"]))


def _legend(commands: list[str], x: float, y: float, items: list[tuple[str, str]]) -> None:
    cursor = x
    for label, color in items:
        commands.append(_rect(cursor, y, 8, 6, color))
        commands.append(_text(cursor + 11, y - 1, label, 6.5, False, COLORS["muted"]))
        cursor += 122


def _donut_slice(commands: list[str], cx: float, cy: float, outer_radius: float, inner_radius: float, start: float, end: float, color: str) -> None:
    steps = max(10, int(abs(end - start) / (pi / 18)))
    outer = [
        (cx + cos(start + (end - start) * step / steps) * outer_radius, cy + sin(start + (end - start) * step / steps) * outer_radius)
        for step in range(steps + 1)
    ]
    inner = [
        (cx + cos(end - (end - start) * step / steps) * inner_radius, cy + sin(end - (end - start) * step / steps) * inner_radius)
        for step in range(steps + 1)
    ]
    commands.append(_polygon(outer + inner, color))


def _line_points(values: list[float | None], x: float, y: float, width: float, height: float, max_value: float) -> list[tuple[float, float]]:
    points = []
    divisor = max(len(values) - 1, 1)
    for index, value in enumerate(values):
        if value is not None:
            points.append((x + index / divisor * width, y + float(value) / max_value * height))
    return points


def _money(value: float, decimals: int = 2) -> str:
    prefix = "-CHF " if value < 0 else "CHF "
    return f"{prefix}{abs(value):,.{decimals}f}".replace(",", "'")


def _compact(value: float) -> str:
    return f"{value:,.0f}".replace(",", "'")


def _clip(value: str, max_length: int) -> str:
    return value if len(value) <= max_length else f"{value[: max_length - 1]}."


def _estimated_text_width(value: str, font_size: float) -> float:
    return len(value) * font_size * 0.48


def _hex_to_rgb(color: str) -> tuple[float, float, float]:
    value = color.lstrip("#")
    return int(value[0:2], 16) / 255, int(value[2:4], 16) / 255, int(value[4:6], 16) / 255


def _rect(x: float, y: float, width: float, height: float, color: str) -> str:
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} rg {x:.1f} {y:.1f} {width:.1f} {height:.1f} re f"


def _stroke_rect(x: float, y: float, width: float, height: float, color: str, line_width: float) -> str:
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {x:.1f} {y:.1f} {width:.1f} {height:.1f} re S"


def _line(points: list[tuple[float, float]], color: str, line_width: float) -> str:
    if len(points) < 2:
        return ""
    r, g, b = _hex_to_rgb(color)
    first_x, first_y = points[0]
    segments = [f"{first_x:.1f} {first_y:.1f} m"]
    segments.extend(f"{point_x:.1f} {point_y:.1f} l" for point_x, point_y in points[1:])
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {' '.join(segments)} S"


def _polygon(points: list[tuple[float, float]], color: str) -> str:
    if len(points) < 3:
        return ""
    r, g, b = _hex_to_rgb(color)
    first_x, first_y = points[0]
    segments = [f"{first_x:.1f} {first_y:.1f} m"]
    segments.extend(f"{point_x:.1f} {point_y:.1f} l" for point_x, point_y in points[1:])
    return f"{r:.3f} {g:.3f} {b:.3f} rg {' '.join(segments)} h f"


def _text(x: float, y: float, text: str, size: float, bold: bool, color: str) -> str:
    font = "F2" if bold else "F1"
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} rg BT /{font} {size:.1f} Tf {x:.1f} {y:.1f} Td ({_escape(text)}) Tj ET"


def _escape(text: str) -> str:
    cleaned = text.encode("latin-1", "replace").decode("latin-1")
    return cleaned.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _stream(commands: list[str]) -> bytes:
    return "\n".join(command for command in commands if command).encode("latin-1", "replace")


def _build_pdf(page_streams: list[bytes]) -> bytes:
    objects: list[bytes | None] = [None]
    objects.extend([b"", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"])
    page_ids = []
    for stream in page_streams:
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
        content_id = len(objects) - 1
        page = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_id} 0 R >>"
        ).encode("ascii")
        objects.append(page)
        page_ids.append(len(objects) - 1)
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    return _serialize(objects)


def _serialize(objects: list[bytes | None]) -> bytes:
    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]
    for object_id, content in enumerate(objects[1:], start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{object_id} 0 obj\n".encode("ascii"))
        pdf.write(content or b"")
        pdf.write(b"\nendobj\n")
    xref_offset = pdf.tell()
    pdf.write(f"xref\n0 {len(objects)}\n".encode("ascii"))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.write(f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii"))
    return pdf.getvalue()
