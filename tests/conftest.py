from datetime import date

import pytest

from budget_app.domain.models import Account, Budget, Transaction


@pytest.fixture
def sample_account() -> Account:
    return Account(id=1, name="Bankkonto", account_type="Bankkonto", starting_balance_chf=1000.0, user_id=1)


@pytest.fixture
def sample_transactions() -> list[Transaction]:
    return [
        Transaction(
            id=1,
            amount_chf=3000.0,
            transaction_type="income",
            transaction_date=date(2026, 4, 1),
            description="Lohn",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=2,
            amount_chf=800.0,
            transaction_type="expense",
            transaction_date=date(2026, 4, 3),
            description="Miete",
            account_id=1,
            category_id=2,
        ),
        Transaction(
            id=3,
            amount_chf=120.0,
            transaction_type="expense",
            transaction_date=date(2026, 4, 8),
            description="Lebensmittel",
            account_id=1,
            category_id=3,
        ),
    ]


@pytest.fixture
def sample_budget() -> Budget:
    return Budget(id=1, month=4, year=2026, limit_chf=500.0, user_id=1, category_id=3)

