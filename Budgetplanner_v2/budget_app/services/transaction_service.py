"""Transaction use cases."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from ..data_access.dao import AccountDAO, CategoryDAO, TransactionDAO
from ..domain.models import Transaction


class TransactionService:
    """Business operations for income and expense transactions."""

    VALID_TYPES = {"income", "expense"}

    def __init__(
        self,
        transaction_dao: TransactionDAO,
        account_dao: AccountDAO,
        category_dao: CategoryDAO,
    ) -> None:
        self.transaction_dao = transaction_dao
        self.account_dao = account_dao
        self.category_dao = category_dao

    def create_transaction(
        self,
        amount_chf: float,
        transaction_type: str,
        transaction_date: date,
        description: str,
        account_id: int,
        category_id: int,
    ) -> Transaction:
        if amount_chf <= 0:
            raise ValueError("Der Betrag muss groesser als 0 sein.")
        if transaction_type not in self.VALID_TYPES:
            raise ValueError("Transaktionstyp muss 'income' oder 'expense' sein.")
        if self.account_dao.get_by_id(account_id) is None:
            raise ValueError("Das ausgewaehlte Konto existiert nicht.")
        if self.category_dao.get_by_id(category_id) is None:
            raise ValueError("Die ausgewaehlte Kategorie existiert nicht.")

        transaction = Transaction(
            amount_chf=round(float(amount_chf), 2),
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            description=description.strip(),
            account_id=account_id,
            category_id=category_id,
        )
        return self.transaction_dao.create(transaction)

    def list_recent(self, limit: int = 200) -> List[Transaction]:
        return self.transaction_dao.list_recent(limit=limit)

    def list_for_month(self, year: int, month: int, user_id: Optional[int] = None) -> List[Transaction]:
        if month < 1 or month > 12:
            raise ValueError("Monat muss zwischen 1 und 12 liegen.")
        return self.transaction_dao.list_for_month(year=year, month=month, user_id=user_id)

