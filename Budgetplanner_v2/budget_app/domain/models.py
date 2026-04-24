"""Domain and ORM models.

The project follows the structure of the Pizzeria reference project: SQLModel is
used as ORM, and the same classes represent domain objects and database tables.

Entities:
- User: owner of accounts, categories and budgets
- Account: money source such as bank account, cash or savings account
- Category: grouping for income and expense transactions
- Transaction: one income or expense entry
- Budget: monthly category limit
"""

from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """Application user.

    The MVP uses one default user, but the model is prepared for several users.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=80)
    email: str = Field(index=True, min_length=3, max_length=120)

    accounts: list["Account"] = Relationship(back_populates="user")
    categories: list["Category"] = Relationship(back_populates="user")
    budgets: list["Budget"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    """A financial account such as bank account, cash or savings account."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=80)
    account_type: str = Field(default="Bankkonto", max_length=40)
    starting_balance_chf: float = Field(default=0.0)
    user_id: int = Field(foreign_key="user.id", index=True)

    user: User = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")


class Category(SQLModel, table=True):
    """A category for grouping transactions and budgets."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=80)
    category_type: str = Field(default="expense", max_length=20)
    user_id: int = Field(foreign_key="user.id", index=True)

    user: User = Relationship(back_populates="categories")
    transactions: list["Transaction"] = Relationship(back_populates="category")
    budgets: list["Budget"] = Relationship(back_populates="category")


class Transaction(SQLModel, table=True):
    """One income or expense.

    Income and expense are represented by ``transaction_type``. This keeps the
    model simple because both variants share the same attributes and behavior.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    amount_chf: float = Field(gt=0)
    transaction_type: str = Field(index=True, max_length=20)
    transaction_date: date = Field(index=True)
    description: str = Field(default="", max_length=200)
    account_id: int = Field(foreign_key="account.id", index=True)
    category_id: int = Field(foreign_key="category.id", index=True)

    account: Account = Relationship(back_populates="transactions")
    category: Category = Relationship(back_populates="transactions")


class Budget(SQLModel, table=True):
    """Monthly spending limit for one category."""

    id: Optional[int] = Field(default=None, primary_key=True)
    month: int = Field(ge=1, le=12, index=True)
    year: int = Field(ge=2000, le=2100, index=True)
    limit_chf: float = Field(gt=0)
    user_id: int = Field(foreign_key="user.id", index=True)
    category_id: int = Field(foreign_key="category.id", index=True)

    user: User = Relationship(back_populates="budgets")
    category: Category = Relationship(back_populates="budgets")
