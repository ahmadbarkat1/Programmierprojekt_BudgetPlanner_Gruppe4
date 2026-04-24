"""UI controllers.

Controllers coordinate between NiceGUI pages and the service layer. They keep the
UI thin and make the application easier to explain in the presentation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

from ..data_access.dao import UserDAO
from ..domain.models import Account, Budget, Category, Transaction, User
from ..services.account_service import AccountService
from ..services.budget_service import BudgetService, BudgetStatus
from ..services.category_service import CategoryService
from ..services.finance_service import FinanceOverview, FinanceService
from ..services.transaction_service import TransactionService


@dataclass(frozen=True)
class DashboardData:
    """All values needed by the dashboard page."""

    user: User
    overview: FinanceOverview
    budget_statuses: List[BudgetStatus]
    transactions: List[Transaction]


class FinanceController:
    """Controller for dashboard and transaction screens."""

    def __init__(
        self,
        user_dao: UserDAO,
        account_service: AccountService,
        category_service: CategoryService,
        transaction_service: TransactionService,
        budget_service: BudgetService,
        finance_service: FinanceService,
    ) -> None:
        self.user_dao = user_dao
        self.account_service = account_service
        self.category_service = category_service
        self.transaction_service = transaction_service
        self.budget_service = budget_service
        self.finance_service = finance_service

    def default_user(self) -> User:
        return self.user_dao.get_default_user()

    def dashboard_data(self, year: int, month: int) -> DashboardData:
        user = self.default_user()
        accounts = self.account_service.list_accounts(user.id)
        transactions = self.transaction_service.list_for_month(year=year, month=month, user_id=user.id)
        budgets = self.budget_service.list_budgets(user.id, year=year, month=month)
        return DashboardData(
            user=user,
            overview=self.finance_service.overview(accounts, transactions),
            budget_statuses=self.budget_service.statuses(budgets, transactions),
            transactions=transactions,
        )

    def list_accounts(self) -> List[Account]:
        return self.account_service.list_accounts(self.default_user().id)

    def list_categories(self, category_type: str | None = None) -> List[Category]:
        return self.category_service.list_categories(self.default_user().id, category_type=category_type)

    def list_recent_transactions(self, limit: int = 200) -> List[Transaction]:
        return self.transaction_service.list_recent(limit=limit)

    def create_account(self, name: str, account_type: str, starting_balance_chf: float) -> Account:
        return self.account_service.create_account(
            name=name,
            account_type=account_type,
            starting_balance_chf=starting_balance_chf,
            user_id=self.default_user().id,
        )

    def create_category(self, name: str, category_type: str) -> Category:
        return self.category_service.create_category(
            name=name,
            category_type=category_type,
            user_id=self.default_user().id,
        )

    def create_transaction(
        self,
        amount_chf: float,
        transaction_type: str,
        transaction_date: date,
        description: str,
        account_id: int,
        category_id: int,
    ) -> Transaction:
        return self.transaction_service.create_transaction(
            amount_chf=amount_chf,
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            description=description,
            account_id=account_id,
            category_id=category_id,
        )

    def create_budget(self, month: int, year: int, limit_chf: float, category_id: int) -> Budget:
        return self.budget_service.create_budget(
            month=month,
            year=year,
            limit_chf=limit_chf,
            user_id=self.default_user().id,
            category_id=category_id,
        )

