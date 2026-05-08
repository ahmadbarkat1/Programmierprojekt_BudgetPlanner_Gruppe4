"""Category use cases."""

from __future__ import annotations

from typing import List, Optional

from ..data_access.dao import CategoryDAO
from ..domain.models import Category


class CategoryService:
    """Business operations for categories."""

    VALID_TYPES = {"income", "expense"}

    def __init__(self, category_dao: CategoryDAO) -> None:
        self.category_dao = category_dao

    def create_category(self, name: str, category_type: str, user_id: int) -> Category:
        if not name.strip():
            raise ValueError("Der Kategoriename darf nicht leer sein.")
        if category_type not in self.VALID_TYPES:
            raise ValueError("Kategorie-Typ muss 'income' oder 'expense' sein.")
        return self.category_dao.create(Category(name=name.strip(), category_type=category_type, user_id=user_id))

    def list_categories(self, user_id: int, category_type: Optional[str] = None) -> List[Category]:
        return self.category_dao.list_for_user(user_id, category_type=category_type)

    def update_category(self, category_id: int, name: str, category_type: str) -> Category:
        if not name.strip():
            raise ValueError("Der Kategoriename darf nicht leer sein.")
        if category_type not in self.VALID_TYPES:
            raise ValueError("Kategorie-Typ muss 'income' oder 'expense' sein.")
        return self.category_dao.update(category_id, name.strip(), category_type)

    def delete_category(self, category_id: int) -> None:
        if self.category_dao.is_used(category_id):
            raise ValueError("Diese Kategorie wird bereits verwendet und kann nicht gelöscht werden.")
        self.category_dao.delete(category_id)
