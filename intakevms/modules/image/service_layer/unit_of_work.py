"""Unit of Work pattern implementation for image management.

This module defines an abstract base class and a SQLAlchemy-based concrete
implementation of the Unit of Work pattern. The Unit of Work pattern helps
manage database transactions and ensures that all operations within a
transaction are completed successfully before committing.

Classes:
    AbstractUnitOfWork: Abstract base class defining the Unit of Work interface.
    SqlAlchemyUnitOfWork: Concrete implementation of the Unit of Work interface
        using SQLAlchemy for database transactions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from intakevms.modules.image.config import DEFAULT_SESSION_FACTORY
from intakevms.modules.image.adapters import repository
from intakevms.common.uow.base_sqlalchemy import BaseSqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from sqlalchemy.orm import sessionmaker

class ImageSqlAlchemyUnitOfWork(BaseSqlAlchemyUnitOfWork):
    """SQLAlchemy-based implementation of the Unit of Work pattern.

    This class manages database transactions using SQLAlchemy.

    Attributes:
        images (ImageSqlAlchemyRepository): Repository for image entities.
    """

    def __init__(self, session_factory: sessionmaker = DEFAULT_SESSION_FACTORY):
        """Initialize the ImageSqlAlchemyUnitOfWork with a session factory.

        Args:
            session_factory (sessionmaker): SQLAlchemy session factory.
                Defaults to DEFAULT_SESSION_FACTORY.
        """
        super().__init__(session_factory)

    def _init_repositories(self) -> None:
        """Initializes repositories for the template module."""
        self.images = repository.ImageSqlAlchemyRepository(self.session)