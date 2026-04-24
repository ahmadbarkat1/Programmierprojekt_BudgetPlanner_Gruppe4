"""Database facade for SQLite + SQLModel.

This is the same idea as in the Pizzeria reference project: one object owns the
engine, creates the schema and seeds start data. The rest of the app does not
create database connections directly.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine, select

from ..data_access.seed import BudgetSeeder
from ..domain.models import User


class Database:
    """Database facade (engine + schema init + session scope)."""

    def __init__(self, database_url: Optional[str] = None, *, echo: bool = False) -> None:
        self._database_url = database_url or os.getenv("DATABASE_URL") or self._default_sqlite_url()
        self._engine: Engine = create_engine(
            self._database_url,
            echo=echo,
            connect_args={"check_same_thread": False},
        )

    @staticmethod
    def _default_sqlite_url() -> str:
        Path("data").mkdir(parents=True, exist_ok=True)
        return "sqlite:///data/budgetplanner.db"

    @property
    def engine(self) -> Engine:
        return self._engine

    def init_schema_and_seed(self) -> None:
        """Create tables and seed demo data if the database is empty."""
        SQLModel.metadata.create_all(self._engine)
        with Session(self._engine) as session:
            if session.exec(select(User)).first() is None:
                BudgetSeeder().seed(session)

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Provide a transactional session scope."""
        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

