"""Structured PDF export for the Budget Planner."""

from __future__ import annotations

from calendar import monthrange
from collections import defaultdict
from io import BytesIO
from math import cos, floor, log10, pi, sin
from typing import TYPE_CHECKING

from ..utils.date_utils import month_name, month_short_label, previous_month, previous_months

if TYPE_CHECKING:
    from ..ui.controllers import FinanceController


PAGE_WIDTH = 595.276
PAGE_HEIGHT = 841.89
MARGIN = 28.3464
CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2

COLORS = {
    "page": "#ffffff",
    "card": "#fcfdff",
    "border": "#e5e7eb",
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
    """Create an A4 portrait PDF and paginate sections when their content grows."""
    selected = [area for area in AREA_ORDER if area in areas]
    pages = []
    for area in selected:
        show_document_title = not pages
        if area == "overview":
            pages.extend(_overview_page(controller, year, month, show_document_title))
        if area == "accounts":
            pages.extend(_accounts_page(controller, year, month, show_document_title))
        if area == "categories":
            pages.extend(_categories_page(controller, year, month, show_document_title))
        if area == "budgets":
            pages.extend(_budgets_page(controller, year, month, show_document_title))
        if area == "transactions":
            pages.extend(_transactions_page(controller, year, month, show_document_title))
    return _build_pdf(pages)


def _base_page(section_title: str, year: int, month: int, show_document_title: bool) -> list[str]:
    commands = [_rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, COLORS["page"])]
    _brand_header(commands, year, month)
    commands.append(_text(MARGIN, 740.7501, section_title, 19, True, COLORS["text"]))
    return commands


def _content_top(show_document_title: bool) -> float:
    return 695.622


def _overview_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> list[bytes]:
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

    chart_gap = 16
    chart_width = (CONTENT_WIDTH - chart_gap) / 2
    _category_chart(commands, MARGIN, 304, 206.85, 248, category_totals)
    _monthly_chart(commands, 238.1102, 304, 328.82, 248, monthly)
    _progress_chart(commands, MARGIN, 25, CONTENT_WIDTH, 268, average, current)
    return [_stream(commands)]


def _accounts_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> list[bytes]:
    accounts = controller.list_accounts()
    transactions = controller.list_recent_transactions()
    total_start = sum(account.starting_balance_chf for account in accounts)
    total_balance = sum(_account_balance(account, transactions) for account in accounts)
    pages: list[bytes] = []

    first_page_slots = 6
    later_page_slots = 9
    chunks = [accounts[:first_page_slots]]
    remaining_accounts = accounts[first_page_slots:]
    chunks.extend(_chunks(remaining_accounts, later_page_slots))
    if not chunks:
        chunks = [[]]

    for page_index, chunk in enumerate(chunks):
        commands = _base_page("Konten", year, month, show_document_title and page_index == 0)
        if page_index == 0:
            commands.append(_text(MARGIN, 686.1577, "Gesamtübersicht", 13, True, COLORS["text"]))
            panel_y = 560.1614
            _summary_card(commands, MARGIN, panel_y, 208.82, 76.5, "Aktueller Gesamtsaldo", _money(total_balance), f"{len(accounts)} Konten aktiv", COLORS["header"])
            _summary_card(commands, 260.4065, panel_y, 141.73, 76.5, "Anzahl Konten", str(len(accounts)), "", COLORS["card"])
            _summary_card(commands, 425.1968, panel_y, 141.73, 76.5, "Gesamter Startsaldo", _money(total_start), "", COLORS["card"])
            grid_top = 510.29
            columns = 3
        else:
            commands.append(_text(MARGIN, 690, f"Weitere Konten ({page_index + 1})", 13, True, COLORS["text"]))
            grid_top = 660
            columns = 3
        _account_grid(commands, chunk, transactions, MARGIN, grid_top, CONTENT_WIDTH, columns)
        pages.append(_stream(commands))
    return pages


def _categories_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> list[bytes]:
    transactions = controller.list_recent_transactions()
    rows = [
        [
            category.name,
            "Einnahme" if category.category_type == "income" else "Ausgabe",
            str(sum(1 for transaction in transactions if transaction.category_id == category.id)),
        ]
        for category in controller.list_categories()
    ]
    return _table_pages("Kategorien", year, month, show_document_title, ["Kategoriename", "Typ", "Verwendungen"], rows, pill_column=1)


def _budgets_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> list[bytes]:
    data = controller.dashboard_data(year=year, month=month)
    budgets = controller.list_budgets(year=year, month=month)
    budget_limit = sum(budget.limit_chf for budget in budgets)
    expenses = sum(transaction.amount_chf for transaction in data.transactions if transaction.transaction_type == "expense")
    remaining = budget_limit - expenses
    usage = expenses / budget_limit * 100 if budget_limit else 0
    pages: list[bytes] = []

    first_page_slots = 8
    later_page_slots = 8
    chunks = [data.budget_statuses[:first_page_slots]]
    chunks.extend(_chunks(data.budget_statuses[first_page_slots:], later_page_slots))
    if not chunks:
        chunks = [[]]

    for page_index, chunk in enumerate(chunks):
        commands = _base_page("Budget", year, month, show_document_title and page_index == 0)
        top = _content_top(show_document_title)
        if page_index == 0:
            _metric_cards(
                commands,
                [
                    ("Budget", _money(budget_limit), COLORS["blue"]),
                    ("Ausgaben", _money(expenses), COLORS["red"]),
                    ("Verbleibend", _money(remaining), COLORS["green"] if remaining >= 0 else COLORS["red"]),
                ],
                top,
                month_name(year, month),
            )
            commands.append(_text(MARGIN, 590, "Budgets für diesen Monat", 13, True, COLORS["text"]))
            card_w = (CONTENT_WIDTH - 24) / 3
            card_h = 130
            for tile_index in range(len(chunk) + 1):
                col = tile_index % 3
                row = tile_index // 3
                x = MARGIN + col * (card_w + 12)
                y = 438 - row * 146
                if tile_index == 0:
                    _budget_total_card(commands, x, y, card_w, card_h, remaining, expenses, budget_limit)
                else:
                    _budget_card(commands, x, y, card_w, card_h, chunk[tile_index - 1])
        else:
            commands.append(_text(MARGIN, 690, f"Weitere Budgets ({page_index + 1})", 13, True, COLORS["text"]))
            _budget_grid(commands, chunk, MARGIN, 650, CONTENT_WIDTH)
        pages.append(_stream(commands))
    return pages


def _transactions_page(controller: "FinanceController", year: int, month: int, show_document_title: bool) -> list[bytes]:
    user = controller.default_user()
    transactions = sorted(
        controller.transaction_service.list_for_month(year=year, month=month, user_id=user.id),
        key=lambda item: (item.transaction_date, item.id or 0),
        reverse=True,
    )
    rows = []
    for transaction in transactions:
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
    return _table_pages(
        "Transaktionen",
        year,
        month,
        show_document_title,
        ["Datum", "Typ", "Kategorie", "Konto", "Beschreibung", "Betrag"],
        rows,
        color_column=5,
        pill_column=1,
        intro=month_name(year, month),
        rows_per_page=27,
    )


def _brand_header(commands: list[str], year: int, month: int) -> None:
    icon_x = MARGIN
    icon_y = 785.8
    _budget_planner_icon(commands, icon_x, icon_y, 22.0)
    commands.append(_text(icon_x + 29.0, 793.0, "Budget Planner", 11.4, True, COLORS["text"]))
    commands.append(_text(484.4937, 795.4589, month_name(year, month), 19, True, COLORS["text"]))


def _budget_planner_icon(commands: list[str], x: float, y: float, size: float) -> None:
    commands.append(_round_rect(x, y, size, size, 2.0, COLORS["teal"]))
    commands.append(_round_rect(x + size * 0.32, y + size * 0.25, size * 0.52, size * 0.50, 1.0, "#ffffff"))
    commands.append(_rect(x + size * 0.50, y + size * 0.39, size * 0.34, size * 0.22, COLORS["teal"]))
    commands.append(_round_rect(x + size * 0.61, y + size * 0.44, size * 0.13, size * 0.13, 0.7, "#ffffff"))


def _account_icon(commands: list[str], x: float, y: float, is_bank: bool) -> None:
    bg = "#dbeafe" if is_bank else "#fef3c7"
    fg = COLORS["blue"] if is_bank else "#92400e"
    commands.append(_round_rect(x, y, 26, 26, 7, bg))
    if is_bank:
        commands.append(_polygon([(x + 5, y + 15), (x + 13, y + 21), (x + 21, y + 15)], fg))
        commands.append(_rect(x + 6, y + 12, 14, 2, fg))
        for col_x in [x + 7, x + 12, x + 17]:
            commands.append(_rect(col_x, y + 7, 2, 5, fg))
        commands.append(_rect(x + 5, y + 5, 16, 2, fg))
    else:
        commands.append(_round_rect(x + 5, y + 8, 16, 11, 2, fg))
        commands.append(_round_rect(x + 8, y + 11, 10, 5, 2, bg))
        commands.append(_rect(x + 7, y + 18, 12, 2, fg))


def _chunks(items: list, size: int) -> list[list]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def _account_grid(commands: list[str], accounts: list, transactions, x: float, top: float, width: float, columns: int) -> None:
    if not accounts:
        _empty_note(commands, x, top - 80, width, "Keine Konten erfasst.")
        return
    gap = 14
    card_h = 164.5 if columns == 3 else 132
    card_w = (width - gap * (columns - 1)) / columns
    for index, account in enumerate(accounts):
        col = index % columns
        row = index // columns
        card_x = x + col * (card_w + gap)
        card_y = top - card_h - row * (card_h + 18)
        _account_card(commands, card_x, card_y, card_w, card_h, account, transactions)


def _summary_card(commands: list[str], x: float, y: float, width: float, height: float, label: str, value: str, detail: str, fill: str) -> None:
    text_color = "#ffffff" if fill == COLORS["header"] else COLORS["text"]
    muted = "#ffffff" if fill == COLORS["header"] else COLORS["muted"]
    commands.append(_round_rect(x, y, width, height, 6, fill))
    if fill != COLORS["header"]:
        commands.append(_stroke_round_rect(x, y, width, height, 6, COLORS["border"], 0.7))
    commands.append(_text(x + 12, y + height - 22, label, 7.2, False, muted))
    commands.append(_text(x + 12, y + 31, _clip(value, 20), 13, True, text_color))
    if detail:
        commands.append(_text(x + 12, y + 14, detail, 8.2, False, muted))


def _budget_grid(commands: list[str], statuses: list, x: float, top: float, width: float) -> None:
    if not statuses:
        _empty_note(commands, x, top - 80, width, "Keine Budgets erfasst.")
        return
    gap = 14
    columns = 2
    card_h = 130
    card_w = (width - gap) / columns
    for index, status in enumerate(statuses):
        col = index % columns
        row = index // columns
        card_x = x + col * (card_w + gap)
        card_y = top - card_h - row * (card_h + 18)
        _budget_card(commands, card_x, card_y, card_w, card_h, status)


def _table_pages(
    section_title: str,
    year: int,
    month: int,
    show_document_title: bool,
    headers: list[str],
    rows: list[list[str]],
    align_right: set[int] | None = None,
    color_column: int | None = None,
    pill_column: int | None = None,
    intro: str | None = None,
    rows_per_page: int = 28,
) -> list[bytes]:
    chunks = _chunks(rows, rows_per_page) or [[]]
    pages: list[bytes] = []
    for page_index, chunk in enumerate(chunks):
        commands = _base_page(section_title, year, month, show_document_title and page_index == 0)
        table_top = 670
        if intro and page_index == 0:
            commands.append(_text(MARGIN, 690, intro, 10, True, COLORS["text"]))
            table_top = 660
        if page_index > 0:
            commands.append(_text(MARGIN, 690, f"Fortsetzung ({page_index + 1})", 10, True, COLORS["muted"]))
        _table(
            commands,
            MARGIN,
            70,
            CONTENT_WIDTH,
            table_top - 70,
            headers,
            chunk,
            align_right=align_right,
            color_column=color_column,
            pill_column=pill_column,
        )
        pages.append(_stream(commands))
    return pages


def _empty_note(commands: list[str], x: float, y: float, width: float, text: str) -> None:
    _card(commands, x, y, width, 78)
    commands.append(_text(x + 16, y + 42, text, 10, True, COLORS["muted"]))


def _metric_cards(commands: list[str], cards: list[tuple[str, str, str]], y: float, subtitle: str = "") -> None:
    gap = 10
    width = (CONTENT_WIDTH - gap * (len(cards) - 1)) / len(cards)
    for index, (label, value, color) in enumerate(cards):
        x = MARGIN + index * (width + gap)
        _card(commands, x, y - 64, width, 64)
        _metric_icon(commands, x + width - 34, y - 36, label, color)
        commands.append(_text(x + 12, y - 22, label, 7.2, False, COLORS["muted"]))
        commands.append(_text(x + 12, y - 44, _clip(value, 18), 14, True, color))
        if subtitle:
            commands.append(_text(x + 12, y - 58, subtitle, 6.2, False, COLORS["muted"]))


def _metric_icon(commands: list[str], x: float, y: float, label: str, color: str) -> None:
    bg = "#dcfce7" if color == COLORS["green"] else "#fee2e2" if color == COLORS["red"] else "#dbeafe"
    commands.append(_round_rect(x, y, 22, 22, 6, bg))
    if "Einnahmen" in label:
        commands.append(_line([(x + 6, y + 8), (x + 11, y + 14), (x + 16, y + 8)], color, 1.7))
        commands.append(_line([(x + 11, y + 14), (x + 11, y + 5)], color, 1.7))
    elif "Ausgaben" in label:
        commands.append(_line([(x + 6, y + 14), (x + 11, y + 8), (x + 16, y + 14)], color, 1.7))
        commands.append(_line([(x + 11, y + 8), (x + 11, y + 17)], color, 1.7))
    else:
        commands.append(_round_rect(x + 5, y + 6, 12, 10, 2, color))
        commands.append(_round_rect(x + 8, y + 9, 6, 4, 1.5, bg))
        commands.append(_rect(x + 7, y + 16, 8, 1.7, color))


def _mini_summary(commands: list[str], x: float, y: float, width: float, height: float, label: str, value: str) -> None:
    commands.append(_rect(x, y, width, height, "#f8fafc"))
    commands.append(_stroke_rect(x, y, width, height, "#e5e7eb", 0.5))
    commands.append(_text(x + 10, y + height - 22, label, 8.2, False, COLORS["muted"]))
    commands.append(_text(x + 10, y + 21, value, 11, True, COLORS["text"]))


def _account_card(commands: list[str], x: float, y: float, width: float, height: float, account, transactions) -> None:
    balance = _account_balance(account, transactions)
    tx_count = sum(1 for transaction in transactions if transaction.account_id == account.id)
    tone = COLORS["green"] if balance >= 0 else COLORS["red"]
    is_bank = account.account_type == "Bankkonto"
    _card(commands, x, y, width, height)
    _account_icon(commands, x + 14, y + height - 42, is_bank)
    commands.append(_text(x + 48, y + height - 22, _clip(account.name, 20), 9, True, COLORS["text"]))
    commands.append(_pill(x + 48, y + height - 41, account.account_type, COLORS["blue"] if is_bank else "#92400e"))
    commands.append(_text(x + 14, y + height - 76, "Aktueller Saldo", 6.4, False, COLORS["muted"]))
    commands.append(_text(x + 14, y + height - 103, _money(balance), 13, True, tone))
    commands.append(_line([(x + 14, y + 58), (x + width - 14, y + 58)], "#d1d5db", 0.45))
    commands.append(_text(x + 14, y + 39, "Startsaldo", 8, False, COLORS["muted"]))
    commands.append(_text(x + width - 86, y + 39, _money(account.starting_balance_chf), 8, True, COLORS["text"]))
    commands.append(_text(x + 14, y + 20, "Transaktionen", 8, False, COLORS["muted"]))
    commands.append(_text(x + width - 26, y + 20, str(tx_count), 8, True, COLORS["text"]))


def _budget_total_card(commands: list[str], x: float, y: float, width: float, height: float, remaining: float, expenses: float, limit: float) -> None:
    usage = expenses / limit * 100 if limit else 0
    tone = COLORS["green"] if remaining >= 0 else COLORS["red"]
    commands.append(_round_rect(x, y, width, height, 6, COLORS["header"]))
    commands.append(_text(x + 10, y + height - 20, "Alle Budgets", 6.5, False, "#ffffff"))
    commands.append(_text(x + 10, y + height - 43, _money(remaining), 13.2, True, "#ffffff"))
    commands.append(_text(x + 10, y + height - 60, f"{_money(expenses)} von {_money(limit)}", 6.2, False, "#ffffff"))
    commands.append(_round_rect(x + 10, y + 56, width - 20, 5, 2.5, "#dbe3ef"))
    commands.append(_round_rect(x + 10, y + 56, (width - 20) * min(max(usage, 0), 100) / 100, 5, 2.5, tone))
    third = (width - 22) / 3
    for index, (label, value, color) in enumerate(
        [
            ("Budget", _money(limit, decimals=0), "#ffffff"),
            ("Verbrauch", _money(expenses, decimals=0), "#ffffff"),
            ("Rest", _money(remaining, decimals=0), "#ffffff"),
        ]
    ):
        box_x = x + 8 + index * (third + 3)
        commands.append(_round_rect(box_x, y + 14, third, 34, 5, "#1f2937"))
        commands.append(_text(box_x + 5, y + 36, label, 5.7, False, "#cbd5e1"))
        commands.append(_text(box_x + 5, y + 22, _clip(value, 9), 6.7, True, color))


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
    cx = x + 61
    cy = y + 99
    radius = 48
    start_angle = -pi / 2
    for index, (_, value) in enumerate(items):
        end_angle = start_angle + 2 * pi * value / total
        _donut_slice(commands, cx, cy, radius, 26, start_angle, end_angle, palette[index % len(palette)])
        start_angle = end_angle
    legend_x = x + 118
    max_label_chars = max(7, int((x + width - legend_x - 16) / 3.1))
    for index, (name, value) in enumerate(items):
        row_y = y + height - 52 - index * 16
        commands.append(_rect(legend_x, row_y, 6, 6, palette[index % len(palette)]))
        commands.append(_text(legend_x + 10, row_y - 1, _clip(name, max_label_chars), 5.8, False, COLORS["muted"]))


def _monthly_chart(commands: list[str], x: float, y: float, width: float, height: float, values: list[dict[str, float | str]]) -> None:
    _panel(commands, x, y, width, height, "Einnahmen vs. Ausgaben")
    if not values:
        commands.append(_text(x + 14, y + height / 2, "Keine Monatsdaten vorhanden.", 8, False, COLORS["muted"]))
        return
    chart_x = x + 38
    chart_y = y + 34
    chart_h = height - 76
    chart_w = width - 58
    raw_max = max(max(float(item["income"]), float(item["expenses"])) for item in values) or 1
    max_value = _nice_axis_max(raw_max)
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
    chart_x = x + 58
    chart_y = y + 48
    chart_w = width - 92
    chart_h = height - 110
    values = average + [value for value in current if value is not None]
    max_value = _nice_axis_max(max(values) if values else 1)
    _grid(commands, chart_x, chart_y, chart_w, chart_h, max_value)
    average_points = _line_points(average, chart_x, chart_y, chart_w, chart_h, max_value)
    current_points = _line_points(current, chart_x, chart_y, chart_w, chart_h, max_value)
    commands.append(_line(average_points, COLORS["muted"], 1.6))
    commands.append(_line(current_points, COLORS["blue"], 1.9))
    for point in average_points:
        commands.append(_circle(point[0], point[1], 1.4, "#ffffff", COLORS["muted"], 0.8))
    for point in current_points:
        commands.append(_circle(point[0], point[1], 1.8, "#ffffff", COLORS["blue"], 0.9))
    commands.append(_text(chart_x + chart_w / 2 - 28, chart_y - 24, "Tage im Monat", 7, True, COLORS["muted"]))
    commands.append(_text_rotated(x + 20, chart_y + chart_h / 2 - 35, "Ausgabe (CHF)", 7, True, COLORS["muted"], 90))
    _line_legend(commands, x + 48, y + height - 36, [("Durchschnitt letzte 3 Monate", COLORS["muted"]), ("Aktuelle Ausgaben", COLORS["blue"])])


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
    commands.append(_round_rect(x, y, width, height, 6, COLORS["card"]))
    commands.append(_stroke_round_rect(x, y, width, height, 6, COLORS["border"], 0.7))


def _pill(x: float, y: float, text: str, color: str) -> str:
    bg = "#dcfce7" if color == COLORS["green"] else "#fee2e2" if color == COLORS["red"] else "#dbeafe" if color == COLORS["blue"] else "#fef3c7"
    width = max(34, _estimated_text_width(text, 6.5) + 13)
    return "\n".join(
        [
            _round_rect(x, y, width, 13, 5, bg),
            _text(x + 5, y + 4, text, 6.5, True, color),
        ]
    )


def _grid(commands: list[str], x: float, y: float, width: float, height: float, max_value: float) -> None:
    commands.append(_line([(x, y), (x + width, y)], "#cbd5e1", 0.5))
    for index in range(1, 4):
        grid_y = y + height * index / 4
        commands.append(_line([(x, grid_y), (x + width, grid_y)], "#e5e7eb", 0.35))
        commands.append(_text(x - 30, grid_y - 2, _compact(max_value * index / 4), 5.7, False, COLORS["muted"]))


def _line_legend(commands: list[str], x: float, y: float, items: list[tuple[str, str]]) -> None:
    cursor = x
    for label, color in items:
        commands.append(_line([(cursor, y + 3), (cursor + 18, y + 3)], color, 1.8))
        commands.append(_circle(cursor + 9, y + 3, 2.2, "#ffffff", color, 1.0))
        commands.append(_text(cursor + 24, y, label, 6.5, False, COLORS["muted"]))
        cursor += max(120, _estimated_text_width(label, 6.5) + 46)


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


def _nice_axis_max(value: float) -> float:
    if value <= 0:
        return 1
    rough_step = value / 4
    magnitude = 10 ** floor(log10(rough_step))
    for multiplier in (1, 2, 5, 10):
        step = multiplier * magnitude
        if step >= rough_step:
            return step * 4
    return rough_step * 4


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


def _rounded_rect_path(x: float, y: float, width: float, height: float, radius: float) -> str:
    r = min(radius, width / 2, height / 2)
    c = r * 0.5522847498
    x0, y0 = x, y
    x1, y1 = x + width, y + height
    return " ".join(
        [
            f"{x0 + r:.1f} {y0:.1f} m",
            f"{x1 - r:.1f} {y0:.1f} l",
            f"{x1 - r + c:.1f} {y0:.1f} {x1:.1f} {y0 + r - c:.1f} {x1:.1f} {y0 + r:.1f} c",
            f"{x1:.1f} {y1 - r:.1f} l",
            f"{x1:.1f} {y1 - r + c:.1f} {x1 - r + c:.1f} {y1:.1f} {x1 - r:.1f} {y1:.1f} c",
            f"{x0 + r:.1f} {y1:.1f} l",
            f"{x0 + r - c:.1f} {y1:.1f} {x0:.1f} {y1 - r + c:.1f} {x0:.1f} {y1 - r:.1f} c",
            f"{x0:.1f} {y0 + r:.1f} l",
            f"{x0:.1f} {y0 + r - c:.1f} {x0 + r - c:.1f} {y0:.1f} {x0 + r:.1f} {y0:.1f} c",
            "h",
        ]
    )


def _round_rect(x: float, y: float, width: float, height: float, radius: float, color: str) -> str:
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} rg {_rounded_rect_path(x, y, width, height, radius)} f"


def _stroke_rect(x: float, y: float, width: float, height: float, color: str, line_width: float) -> str:
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {x:.1f} {y:.1f} {width:.1f} {height:.1f} re S"


def _stroke_round_rect(x: float, y: float, width: float, height: float, radius: float, color: str, line_width: float) -> str:
    r, g, b = _hex_to_rgb(color)
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {_rounded_rect_path(x, y, width, height, radius)} S"


def _line(points: list[tuple[float, float]], color: str, line_width: float) -> str:
    if len(points) < 2:
        return ""
    r, g, b = _hex_to_rgb(color)
    first_x, first_y = points[0]
    segments = [f"{first_x:.1f} {first_y:.1f} m"]
    segments.extend(f"{point_x:.1f} {point_y:.1f} l" for point_x, point_y in points[1:])
    return f"{r:.3f} {g:.3f} {b:.3f} RG {line_width:.1f} w {' '.join(segments)} S"


def _circle(x: float, y: float, radius: float, fill_color: str, stroke_color: str | None = None, line_width: float = 0.7) -> str:
    fill_r, fill_g, fill_b = _hex_to_rgb(fill_color)
    c = radius * 0.5522847498
    path = " ".join(
        [
            f"{x + radius:.1f} {y:.1f} m",
            f"{x + radius:.1f} {y + c:.1f} {x + c:.1f} {y + radius:.1f} {x:.1f} {y + radius:.1f} c",
            f"{x - c:.1f} {y + radius:.1f} {x - radius:.1f} {y + c:.1f} {x - radius:.1f} {y:.1f} c",
            f"{x - radius:.1f} {y - c:.1f} {x - c:.1f} {y - radius:.1f} {x:.1f} {y - radius:.1f} c",
            f"{x + c:.1f} {y - radius:.1f} {x + radius:.1f} {y - c:.1f} {x + radius:.1f} {y:.1f} c",
            "h",
        ]
    )
    if stroke_color:
        stroke_r, stroke_g, stroke_b = _hex_to_rgb(stroke_color)
        return f"{fill_r:.3f} {fill_g:.3f} {fill_b:.3f} rg {stroke_r:.3f} {stroke_g:.3f} {stroke_b:.3f} RG {line_width:.1f} w {path} B"
    return f"{fill_r:.3f} {fill_g:.3f} {fill_b:.3f} rg {path} f"


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


def _text_rotated(x: float, y: float, text: str, size: float, bold: bool, color: str, angle: int) -> str:
    font = "F2" if bold else "F1"
    r, g, b = _hex_to_rgb(color)
    if angle == 90:
        matrix = f"0 1 -1 0 {x:.1f} {y:.1f}"
    elif angle == -90:
        matrix = f"0 -1 1 0 {x:.1f} {y:.1f}"
    else:
        matrix = f"1 0 0 1 {x:.1f} {y:.1f}"
    return f"{r:.3f} {g:.3f} {b:.3f} rg BT /{font} {size:.1f} Tf {matrix} Tm ({_escape(text)}) Tj ET"


def _escape(text: str) -> str:
    cleaned = text.encode("latin-1", "replace").decode("latin-1")
    return cleaned.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _stream(commands: list[str]) -> bytes:
    return "\n".join(command for command in commands if command).encode("latin-1", "replace")


def _build_pdf(page_streams: list[bytes]) -> bytes:
    objects: list[bytes | None] = [None]
    objects.extend([b"", b"", b"<< /Type /Font /Subtype /TrueType /BaseFont /SegoeUI /Encoding /WinAnsiEncoding >>", b"<< /Type /Font /Subtype /TrueType /BaseFont /SegoeUI-Bold /Encoding /WinAnsiEncoding >>"])
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
