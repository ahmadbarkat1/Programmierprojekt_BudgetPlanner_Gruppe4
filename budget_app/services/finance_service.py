"""Finance calculations.

This service is deliberately independent from NiceGUI and SQLModel sessions. That
makes the business rules easy to understand and easy to test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..domain.models import Account, Transaction


@dataclass(frozen=True)
class FinanceOverview:
    """Aggregated values shown on the dashboard."""

    total_income_chf: float
    total_expenses_chf: float
    balance_chf: float


class FinanceService:
    """Calculates balances, income and expenses."""

    @staticmethod
    def signed_amount(transaction: Transaction) -> float:
        """Return positive income and negative expense amount."""
        if transaction.transaction_type == "income":
            return round(transaction.amount_chf, 2)
        if transaction.transaction_type == "expense":
            return round(-transaction.amount_chf, 2)
        raise ValueError(f"Unknown transaction type: {transaction.transaction_type}")

    def total_income(self, transactions: Iterable[Transaction]) -> float:
        return round(sum(t.amount_chf for t in transactions if t.transaction_type == "income"), 2)

    def total_expenses(self, transactions: Iterable[Transaction]) -> float:
        return round(sum(t.amount_chf for t in transactions if t.transaction_type == "expense"), 2)

    def account_balance(self, account: Account, transactions: Iterable[Transaction]) -> float:
        changes = sum(self.signed_amount(t) for t in transactions if t.account_id == account.id)
        return round(account.starting_balance_chf + changes, 2)

    def overview(self, accounts: Iterable[Account], transactions: Iterable[Transaction]) -> FinanceOverview:
        transaction_list = list(transactions)
        starting_balance = sum(account.starting_balance_chf for account in accounts)
        income = self.total_income(transaction_list)
        expenses = self.total_expenses(transaction_list)
        balance = round(starting_balance + income - expenses, 2)
        return FinanceOverview(total_income_chf=income, total_expenses_chf=expenses, balance_chf=balance)

