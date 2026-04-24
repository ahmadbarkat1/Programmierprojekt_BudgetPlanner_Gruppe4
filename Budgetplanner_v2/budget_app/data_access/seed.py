"""Seed data for first application start."""

from sqlmodel import Session

from ..domain.models import Account, Category, User


class BudgetSeeder:
    """Creates useful start data for demos and first use."""

    def seed(self, session: Session) -> User:
        user = User(name="Demo User", email="demo@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)

        accounts = [
            Account(name="Bankkonto", account_type="Bankkonto", starting_balance_chf=1200.0, user_id=user.id),
            Account(name="Bargeld", account_type="Bargeld", starting_balance_chf=150.0, user_id=user.id),
        ]
        categories = [
            Category(name="Lohn", category_type="income", user_id=user.id),
            Category(name="Nebenjob", category_type="income", user_id=user.id),
            Category(name="Miete", category_type="expense", user_id=user.id),
            Category(name="Lebensmittel", category_type="expense", user_id=user.id),
            Category(name="Freizeit", category_type="expense", user_id=user.id),
            Category(name="Transport", category_type="expense", user_id=user.id),
        ]

        session.add_all(accounts + categories)
        session.commit()
        return user

