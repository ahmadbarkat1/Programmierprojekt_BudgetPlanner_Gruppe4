from budget_app.domain.models import Account
from budget_app.services.budget_service import BudgetService
from budget_app.services.finance_service import FinanceService
from budget_app.services.recurrence_service import RecurrenceService


def test_finance_overview(sample_account, sample_transactions):
    finance = FinanceService()
    overview = finance.overview([sample_account], sample_transactions)

    assert overview.total_income_chf == 3000.0
    assert overview.total_expenses_chf == 920.0
    assert overview.balance_chf == 3080.0


def test_account_balance(sample_account, sample_transactions):
    finance = FinanceService()

    assert finance.account_balance(sample_account, sample_transactions) == 3080.0


def test_finance_overview_without_transactions_uses_starting_balances():
    accounts = [
        Account(id=1, name="Bankkonto", account_type="Bankkonto", starting_balance_chf=1200.0, user_id=1),
        Account(id=2, name="Bargeld", account_type="Bargeld", starting_balance_chf=150.0, user_id=1),
    ]

    overview = FinanceService().overview(accounts, [])

    assert overview.total_income_chf == 0.0
    assert overview.total_expenses_chf == 0.0
    assert overview.balance_chf == 1350.0


def test_budget_status_not_exceeded(sample_budget, sample_transactions):
    budget_service = BudgetService(budget_dao=None, category_dao=None)
    status = budget_service.status_for_budget(sample_budget, sample_transactions)

    assert status.spent_chf == 120.0
    assert status.remaining_chf == 380.0
    assert status.is_exceeded is False


def test_budget_status_exceeded(sample_budget, sample_transactions):
    sample_budget.limit_chf = 100.0
    budget_service = BudgetService(budget_dao=None, category_dao=None)
    status = budget_service.status_for_budget(sample_budget, sample_transactions)

    assert status.spent_chf == 120.0
    assert status.remaining_chf == -20.0
    assert status.is_exceeded is True


def test_quarterly_recurrence_dates():
    dates = RecurrenceService.dates(sample_transactions_start_date(), "quarterly", 4)

    assert [value.isoformat() for value in dates] == ["2026-01-31", "2026-04-30", "2026-07-30", "2026-10-30"]


def sample_transactions_start_date():
    from datetime import date

    return date(2026, 1, 31)
