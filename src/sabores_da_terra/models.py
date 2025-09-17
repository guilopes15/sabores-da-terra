from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class OrderStatus(str, Enum):
    pending = 'pending'
    canceled = 'canceled'
    paid = 'paid'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    orders: Mapped[list['Order']] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )


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


@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint(
            'total_amount > 0', name='check_total_amount_positive'
        ),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    total_amount: Mapped[Decimal] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        nullable=False, default=OrderStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    items: Mapped[list['OrderItem']] = relationship(
        init=False, cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class OrderItem:
    __tablename__ = 'order_items'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    product: Mapped['Product'] = relationship(init=False)
