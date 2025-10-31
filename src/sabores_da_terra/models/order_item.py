from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_registry import table_registry

if TYPE_CHECKING:
    from .product import Product


@table_registry.mapped_as_dataclass
class OrderItem:
    __tablename__ = 'order_items'
    __table_args__ = (CheckConstraint('quantity >= 0', name='check_quantity'),)

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    product_name: Mapped[str] = mapped_column(nullable=False, default='')
    product_image: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )
    product: Mapped['Product'] = relationship(init=False)
