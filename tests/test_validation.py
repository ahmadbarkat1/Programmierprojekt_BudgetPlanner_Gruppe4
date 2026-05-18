import pytest
from datetime import date

from budget_app.services.transaction_service import TransactionService


class FailingDAO:
    def get_by_id(self, item_id):
        raise AssertionError("DAO should not be called for basic validation failures")


def setup_services():
    return TransactionService(
        transaction_dao=FailingDAO(),
        account_dao=FailingDAO(),
        category_dao=FailingDAO(),
    )


def test_transaction_invalid_amount():
    service = setup_services()

    with pytest.raises(ValueError):
        service.create_transaction(
            amount_chf=0,
            transaction_type="expense",
            transaction_date=date.today(),
            description="Test",
            account_id=1,
            category_id=1,
        )


def test_transaction_invalid_type():
    service = setup_services()

    with pytest.raises(ValueError):
        service.create_transaction(
            amount_chf=10,
            transaction_type="invalid",
            transaction_date=date.today(),
            description="Test",
            account_id=1,
            category_id=1,
        )
