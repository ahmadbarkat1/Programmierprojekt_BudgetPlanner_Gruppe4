"""DAO classes for persistence.

The services and UI do not know raw SQL or SQLModel sessions. DAOs encapsulate
CRUD operations and queries behind class-based interfaces.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from ..domain.models import Account, Budget, Category, Transaction, User


class BaseDAO:
    """Base class holding the SQLAlchemy/SQLModel engine."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        """Create a new database session."""
        return Session(self.engine)


class UserDAO(BaseDAO):
    """DAO for user data."""

    def get_default_user(self) -> User:
        with self.session() as session:
            user = session.exec(select(User).order_by(User.id)).first()
            if user is None:
                user = User(name="Demo User", email="demo@example.com")
                session.add(user)
                session.commit()
                session.refresh(user)
            return user


class AccountDAO(BaseDAO):
    """DAO for account persistence."""

    def create(self, account: Account) -> Account:
        with self.session() as session:
            session.add(account)
            session.commit()
            session.refresh(account)
            return account

    def list_for_user(self, user_id: int) -> List[Account]:
        with self.session() as session:
            statement = select(Account).where(Account.user_id == user_id).order_by(Account.name)
            return list(session.exec(statement).all())

    def get_by_id(self, account_id: int) -> Optional[Account]:
        with self.session() as session:
            return session.get(Account, account_id)


class CategoryDAO(BaseDAO):
    """DAO for categories."""

    def create(self, category: Category) -> Category:
        with self.session() as session:
            session.add(category)
            session.commit()
            session.refresh(category)
            return category

    def list_for_user(self, user_id: int, category_type: Optional[str] = None) -> List[Category]:
        with self.session() as session:
            statement = select(Category).where(Category.user_id == user_id)
            if category_type:
                statement = statement.where(Category.category_type == category_type)
            statement = statement.order_by(Category.category_type, Category.name)
            return list(session.exec(statement).all())

    def get_by_id(self, category_id: int) -> Optional[Category]:
        with self.session() as session:
            return session.get(Category, category_id)


class TransactionDAO(BaseDAO):
    """DAO for transaction persistence and queries."""

    def create(self, transaction: Transaction) -> Transaction:
        with self.session() as session:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return transaction

    def list_recent(self, limit: int = 200) -> List[Transaction]:
        with self.session() as session:
            statement = select(Transaction).order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).limit(limit)
            transactions = list(session.exec(statement).all())
            for transaction in transactions:
                _ = transaction.account
                _ = transaction.category
            return transactions

    def list_for_month(self, year: int, month: int, user_id: Optional[int] = None) -> List[Transaction]:
        start = date(year, month, 1)
        end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        with self.session() as session:
            statement = (
                select(Transaction)
                .join(Account)
                .where(Transaction.transaction_date >= start)
                .where(Transaction.transaction_date < end)
            )
            if user_id is not None:
                statement = statement.where(Account.user_id == user_id)
            transactions = list(session.exec(statement).all())
            for transaction in transactions:
                _ = transaction.account
                _ = transaction.category
            return transactions


class BudgetDAO(BaseDAO):
    """DAO for monthly budgets."""

    def create(self, budget: Budget) -> Budget:
        with self.session() as session:
            session.add(budget)
            session.commit()
            session.refresh(budget)
            return budget

    def list_for_user(self, user_id: int, year: Optional[int] = None, month: Optional[int] = None) -> List[Budget]:
        with self.session() as session:
            statement = select(Budget).where(Budget.user_id == user_id)
            if year is not None:
                statement = statement.where(Budget.year == year)
            if month is not None:
                statement = statement.where(Budget.month == month)
            statement = statement.order_by(Budget.year.desc(), Budget.month.desc())
            budgets = list(session.exec(statement).all())
            for budget in budgets:
                _ = budget.category
            return budgets

    def get_by_category_month(self, user_id: int, category_id: int, year: int, month: int) -> Optional[Budget]:
        with self.session() as session:
            statement = (
                select(Budget)
                .where(Budget.user_id == user_id)
                .where(Budget.category_id == category_id)
                .where(Budget.year == year)
                .where(Budget.month == month)
            )
            return session.exec(statement).first()

