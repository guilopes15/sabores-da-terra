from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .model_registry import table_registry


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint(
            'stock_quantity >= 0', name='check_stock_non_negative'
        ),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )
    price: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    stock_quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
