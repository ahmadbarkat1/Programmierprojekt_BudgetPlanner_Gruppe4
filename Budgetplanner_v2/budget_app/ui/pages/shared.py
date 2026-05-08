"""Page-local shared helpers."""

from __future__ import annotations

from ..controllers import FinanceController
from ...domain.models import Account, Category, Transaction


def account_balance(account: Account, transactions: list[Transaction]) -> float:
    balance = account.starting_balance_chf
    for transaction in transactions:
        if transaction.account_id != account.id:
            continue
        if transaction.transaction_type == "income":
            balance += transaction.amount_chf
        else:
            balance -= transaction.amount_chf
    return round(balance, 2)


def usage_count(items: list[Transaction], attribute: str, item_id: int | None) -> int:
    return sum(1 for item in items if getattr(item, attribute) == item_id)


def category_type_label(category: Category) -> str:
    return "Einnahme" if category.category_type == "income" else "Ausgabe"


def dashboard_month(controller: FinanceController, year: int, month: int):
    return controller.dashboard_data(year=year, month=month)
