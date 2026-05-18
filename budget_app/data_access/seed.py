"""Seed data for first application start."""

from datetime import date

from sqlmodel import select
from sqlmodel import Session

from ..domain.models import Account, Budget, Category, Transaction, User


class BudgetSeeder:
    """Creates useful start data for demos and first use."""

    def seed(self, session: Session) -> User:
        user = User(name="Luca Student", email="luca.student@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)

        accounts = [
            Account(name="Studentenkonto", account_type="Bankkonto", starting_balance_chf=950.0, user_id=user.id),
            Account(name="Bargeld", account_type="Bargeld", starting_balance_chf=80.0, user_id=user.id),
        ]
        categories = [
            Category(name="Nebenjob", category_type="income", user_id=user.id),
            Category(name="Nachhilfe", category_type="income", user_id=user.id),
            Category(name="Miete", category_type="expense", user_id=user.id),
            Category(name="Lebensmittel", category_type="expense", user_id=user.id),
            Category(name="Fast Food", category_type="expense", user_id=user.id),
            Category(name="Ausgang", category_type="expense", user_id=user.id),
            Category(name="Padel", category_type="expense", user_id=user.id),
            Category(name="Transport", category_type="expense", user_id=user.id),
            Category(name="Studium", category_type="expense", user_id=user.id),
        ]

        session.add_all(accounts + categories)
        session.commit()
        self.seed_demo_activity(session, user)
        return user

    def seed_demo_activity(self, session: Session, user: User) -> None:
        """Add realistic demo budgets and transactions for a Swiss student."""
        if user.email == "demo@example.com":
            user.name = "Luca Student"
            user.email = "luca.student@example.com"
            session.add(user)
            session.commit()

        accounts = self._accounts_by_name(session, user.id)
        categories = self._categories_by_name(session, user.id)
        required_accounts = [
            Account(name="Studentenkonto", account_type="Bankkonto", starting_balance_chf=950.0, user_id=user.id),
            Account(name="Bargeld", account_type="Bargeld", starting_balance_chf=80.0, user_id=user.id),
        ]
        required_categories = [
            Category(name="Nebenjob", category_type="income", user_id=user.id),
            Category(name="Nachhilfe", category_type="income", user_id=user.id),
            Category(name="Miete", category_type="expense", user_id=user.id),
            Category(name="Lebensmittel", category_type="expense", user_id=user.id),
            Category(name="Fast Food", category_type="expense", user_id=user.id),
            Category(name="Ausgang", category_type="expense", user_id=user.id),
            Category(name="Padel", category_type="expense", user_id=user.id),
            Category(name="Transport", category_type="expense", user_id=user.id),
            Category(name="Studium", category_type="expense", user_id=user.id),
        ]
        for account in required_accounts:
            if account.name not in accounts:
                session.add(account)
        for category in required_categories:
            if category.name not in categories:
                session.add(category)
        session.commit()

        accounts = self._accounts_by_name(session, user.id)
        categories = self._categories_by_name(session, user.id)
        bank_account = accounts.get("Studentenkonto") or accounts.get("Bankkonto")
        cash_account = accounts["Bargeld"]

        stale_demo_transaction = session.exec(
            select(Transaction)
            .where(Transaction.description == "Padel und Leihschläger")
            .where(Transaction.transaction_date == date(2026, 5, 21))
        ).first()
        if stale_demo_transaction is not None:
            session.delete(stale_demo_transaction)
        old_may_salary = session.exec(
            select(Transaction)
            .where(Transaction.description == "Monatslohn Nebenjob")
            .where(Transaction.transaction_date == date(2026, 5, 1))
        ).first()
        if old_may_salary is not None:
            session.delete(old_may_salary)

        budget_limits = {
            "Miete": 850.0,
            "Lebensmittel": 420.0,
            "Fast Food": 130.0,
            "Ausgang": 180.0,
            "Padel": 120.0,
            "Transport": 95.0,
            "Studium": 160.0,
        }
        for month in range(1, 6):
            for category_name, limit in budget_limits.items():
                self._add_budget_if_missing(session, user.id, categories[category_name].id, 2026, month, limit)

        monthly_transactions = {
            1: [
                (2600.0, "income", 1, "Monatslohn Nebenjob Januar", bank_account.id, "Nebenjob"),
                (80.0, "income", 7, "Nachhilfe Mathematik", bank_account.id, "Nachhilfe"),
                (90.0, "income", 21, "Nachhilfe Prüfungsvorbereitung", bank_account.id, "Nachhilfe"),
                (820.0, "expense", 2, "WG-Zimmer Miete", bank_account.id, "Miete"),
                (95.30, "expense", 4, "Wocheneinkauf Migros", bank_account.id, "Lebensmittel"),
                (71.50, "expense", 12, "Wocheneinkauf Coop", bank_account.id, "Lebensmittel"),
                (16.90, "expense", 9, "Burger nach Vorlesung", cash_account.id, "Fast Food"),
                (48.0, "expense", 17, "Ausgang Winterthur", bank_account.id, "Ausgang"),
                (32.0, "expense", 24, "Padelplatz mit Freunden", bank_account.id, "Padel"),
                (59.0, "expense", 5, "ÖV Monatsanteil", bank_account.id, "Transport"),
                (58.20, "expense", 15, "Skript und Lernmaterial", bank_account.id, "Studium"),
            ],
            2: [
                (2600.0, "income", 1, "Monatslohn Nebenjob Februar", bank_account.id, "Nebenjob"),
                (100.0, "income", 5, "Nachhilfe Rechnungswesen", bank_account.id, "Nachhilfe"),
                (85.0, "income", 19, "Nachhilfe Mathematik", bank_account.id, "Nachhilfe"),
                (820.0, "expense", 2, "WG-Zimmer Miete", bank_account.id, "Miete"),
                (88.70, "expense", 3, "Wocheneinkauf Migros", bank_account.id, "Lebensmittel"),
                (76.40, "expense", 14, "Wocheneinkauf Coop", bank_account.id, "Lebensmittel"),
                (19.50, "expense", 8, "Döner mit Kommilitonen", cash_account.id, "Fast Food"),
                (61.0, "expense", 22, "Ausgang Zürich", bank_account.id, "Ausgang"),
                (36.0, "expense", 16, "Padel und Leihschläger", bank_account.id, "Padel"),
                (59.0, "expense", 5, "ÖV Monatsanteil", bank_account.id, "Transport"),
                (39.90, "expense", 11, "Notizbuch und Druckkosten", bank_account.id, "Studium"),
            ],
            3: [
                (2600.0, "income", 1, "Monatslohn Nebenjob März", bank_account.id, "Nebenjob"),
                (90.0, "income", 6, "Nachhilfe Mathematik", bank_account.id, "Nachhilfe"),
                (90.0, "income", 20, "Nachhilfe Prüfungsvorbereitung", bank_account.id, "Nachhilfe"),
                (820.0, "expense", 2, "WG-Zimmer Miete", bank_account.id, "Miete"),
                (102.10, "expense", 4, "Wocheneinkauf Migros", bank_account.id, "Lebensmittel"),
                (82.30, "expense", 15, "Wocheneinkauf Coop", bank_account.id, "Lebensmittel"),
                (18.90, "expense", 7, "Burger nach Vorlesung", cash_account.id, "Fast Food"),
                (22.50, "expense", 18, "Pizza nach Training", cash_account.id, "Fast Food"),
                (73.0, "expense", 23, "Ausgang Zürich", bank_account.id, "Ausgang"),
                (34.0, "expense", 13, "Padelplatz mit Freunden", bank_account.id, "Padel"),
                (59.0, "expense", 5, "ÖV Monatsanteil", bank_account.id, "Transport"),
                (64.50, "expense", 12, "Fachbuch gebraucht", bank_account.id, "Studium"),
            ],
            4: [
                (2600.0, "income", 1, "Monatslohn Nebenjob April", bank_account.id, "Nebenjob"),
                (80.0, "income", 8, "Nachhilfe Rechnungswesen", bank_account.id, "Nachhilfe"),
                (100.0, "income", 22, "Nachhilfe Mathematik", bank_account.id, "Nachhilfe"),
                (820.0, "expense", 2, "WG-Zimmer Miete", bank_account.id, "Miete"),
                (91.60, "expense", 3, "Wocheneinkauf Migros", bank_account.id, "Lebensmittel"),
                (78.80, "expense", 13, "Wocheneinkauf Coop", bank_account.id, "Lebensmittel"),
                (14.50, "expense", 10, "Döner mit Kommilitonen", cash_account.id, "Fast Food"),
                (17.90, "expense", 25, "Burger nach Vorlesung", cash_account.id, "Fast Food"),
                (55.0, "expense", 19, "Ausgang Winterthur", bank_account.id, "Ausgang"),
                (34.0, "expense", 16, "Padelplatz mit Freunden", bank_account.id, "Padel"),
                (28.0, "expense", 28, "Padel und Leihschläger", bank_account.id, "Padel"),
                (59.0, "expense", 5, "ÖV Monatsanteil", bank_account.id, "Transport"),
                (42.0, "expense", 9, "Skript und Lernmaterial", bank_account.id, "Studium"),
            ],
            5: [
                (2600.0, "income", 1, "Monatslohn Nebenjob Mai", bank_account.id, "Nebenjob"),
                (90.0, "income", 4, "Nachhilfe Mathematik", bank_account.id, "Nachhilfe"),
                (80.0, "income", 11, "Nachhilfe Rechnungswesen", bank_account.id, "Nachhilfe"),
                (100.0, "income", 18, "Nachhilfe Prüfungsvorbereitung", bank_account.id, "Nachhilfe"),
                (820.0, "expense", 2, "WG-Zimmer Miete", bank_account.id, "Miete"),
                (86.40, "expense", 3, "Wocheneinkauf Migros", bank_account.id, "Lebensmittel"),
                (74.20, "expense", 10, "Wocheneinkauf Coop", bank_account.id, "Lebensmittel"),
                (18.90, "expense", 6, "Burger nach Vorlesung", cash_account.id, "Fast Food"),
                (14.50, "expense", 15, "Döner mit Kommilitonen", cash_account.id, "Fast Food"),
                (52.0, "expense", 9, "Ausgang Zürich", bank_account.id, "Ausgang"),
                (34.0, "expense", 17, "Padelplatz mit Freunden", bank_account.id, "Padel"),
                (59.0, "expense", 5, "ÖV Monatsanteil", bank_account.id, "Transport"),
                (46.80, "expense", 13, "Skript und Lernmaterial", bank_account.id, "Studium"),
            ],
        }
        for month, transactions in monthly_transactions.items():
            for amount, transaction_type, day, description, account_id, category_name in transactions:
                self._add_transaction_if_missing(
                    session=session,
                    amount_chf=amount,
                    transaction_type=transaction_type,
                    transaction_date=date(2026, month, day),
                    description=description,
                    account_id=account_id,
                    category_id=categories[category_name].id,
                )
        session.commit()

    @staticmethod
    def _accounts_by_name(session: Session, user_id: int) -> dict[str, Account]:
        accounts = session.exec(select(Account).where(Account.user_id == user_id)).all()
        return {account.name: account for account in accounts}

    @staticmethod
    def _categories_by_name(session: Session, user_id: int) -> dict[str, Category]:
        categories = session.exec(select(Category).where(Category.user_id == user_id)).all()
        return {category.name: category for category in categories}

    @staticmethod
    def _add_budget_if_missing(
        session: Session,
        user_id: int,
        category_id: int,
        year: int,
        month: int,
        limit_chf: float,
    ) -> None:
        existing_budget = session.exec(
            select(Budget)
            .where(Budget.user_id == user_id)
            .where(Budget.category_id == category_id)
            .where(Budget.year == year)
            .where(Budget.month == month)
        ).first()
        if existing_budget is None:
            session.add(Budget(month=month, year=year, limit_chf=limit_chf, user_id=user_id, category_id=category_id))

    @staticmethod
    def _add_transaction_if_missing(
        session: Session,
        amount_chf: float,
        transaction_type: str,
        transaction_date: date,
        description: str,
        account_id: int,
        category_id: int,
    ) -> None:
        existing_transaction = session.exec(
            select(Transaction)
            .where(Transaction.transaction_date == transaction_date)
            .where(Transaction.description == description)
            .where(Transaction.amount_chf == amount_chf)
        ).first()
        if existing_transaction is None:
            session.add(
                Transaction(
                    amount_chf=amount_chf,
                    transaction_type=transaction_type,
                    transaction_date=transaction_date,
                    description=description,
                    account_id=account_id,
                    category_id=category_id,
                )
            )
