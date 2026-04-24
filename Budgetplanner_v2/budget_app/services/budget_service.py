"""Budget use cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..data_access.dao import BudgetDAO, CategoryDAO
from ..domain.models import Budget, Transaction


@dataclass(frozen=True)
class BudgetStatus:
    """Status of one monthly category budget."""

    budget: Budget
    spent_chf: float
    remaining_chf: float
    is_exceeded: bool


class BudgetService:
    """Business operations for monthly budgets."""

    def __init__(self, budget_dao: BudgetDAO, category_dao: CategoryDAO) -> None:
        self.budget_dao = budget_dao
        self.category_dao = category_dao

    def create_budget(self, month: int, year: int, limit_chf: float, user_id: int, category_id: int) -> Budget:
        if month < 1 or month > 12:
            raise ValueError("Monat muss zwischen 1 und 12 liegen.")
        if year < 2000:
            raise ValueError("Jahr ist ungueltig.")
        if limit_chf <= 0:
            raise ValueError("Budgetlimite muss groesser als 0 sein.")
        category = self.category_dao.get_by_id(category_id)
        if category is None:
            raise ValueError("Die ausgewaehlte Kategorie existiert nicht.")
        if category.category_type != "expense":
            raise ValueError("Budgets koennen nur fuer Ausgabenkategorien erstellt werden.")

        existing = self.budget_dao.get_by_category_month(user_id, category_id, year, month)
        if existing is not None:
            raise ValueError("Fuer diese Kategorie und diesen Monat gibt es bereits ein Budget.")

        return self.budget_dao.create(
            Budget(
                month=month,
                year=year,
                limit_chf=round(float(limit_chf), 2),
                user_id=user_id,
                category_id=category_id,
            )
        )

    def list_budgets(self, user_id: int, year: Optional[int] = None, month: Optional[int] = None) -> List[Budget]:
        return self.budget_dao.list_for_user(user_id=user_id, year=year, month=month)

    def spent_for_budget(self, budget: Budget, transactions: Iterable[Transaction]) -> float:
        spent = sum(
            transaction.amount_chf
            for transaction in transactions
            if transaction.transaction_type == "expense" and transaction.category_id == budget.category_id
        )
        return round(spent, 2)

    def status_for_budget(self, budget: Budget, transactions: Iterable[Transaction]) -> BudgetStatus:
        spent = self.spent_for_budget(budget, transactions)
        remaining = round(budget.limit_chf - spent, 2)
        return BudgetStatus(
            budget=budget,
            spent_chf=spent,
            remaining_chf=remaining,
            is_exceeded=remaining < 0,
        )

    def statuses(self, budgets: Iterable[Budget], transactions: Iterable[Transaction]) -> List[BudgetStatus]:
        transaction_list = list(transactions)
        return [self.status_for_budget(budget, transaction_list) for budget in budgets]

