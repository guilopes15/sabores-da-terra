from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import CheckConstraint, delete, event, func, select, update
from sqlalchemy.orm import Mapped, attributes, mapped_column

from .model_registry import table_registry
from .order import Order
from .order_item import OrderItem


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
    is_active: Mapped[bool] = mapped_column(init=False, default=True)
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@event.listens_for(Product, 'after_update')
def remove_product_from_pending_orders(mapper, connection, target):
    history = attributes.get_history(target, 'is_active')
    if (
        history.has_changes()
        and history.deleted == [True]
        and history.added == [False]
    ):
        query = delete(OrderItem).where(
            (OrderItem.product_id == target.id)
            & (
                OrderItem.order_id.in_(
                    select(Order.id).where(Order.status == 'pending')
                )
            )
        )

        connection.execute(query)

        # Atualiza o total_amount dos pedidos 
        query = (
            update(Order)
            .where(Order.status == 'pending')
            .values(
                total_amount=(
                    select(func.coalesce(
                        func.sum(OrderItem.quantity * OrderItem.price), 0))
                    .where(OrderItem.order_id == Order.id)
                    .scalar_subquery()
                )
            )
        )

        connection.execute(query)
