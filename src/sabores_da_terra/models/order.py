from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_registry import table_registry
#from .order_item import OrderItem


class OrderStatus(str, Enum):
    pending = 'pending'
    canceled = 'canceled'
    paid = 'paid'


@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='check_total_amount'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    total_amount: Mapped[Decimal] = mapped_column(nullable=False, default=0)
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
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )
