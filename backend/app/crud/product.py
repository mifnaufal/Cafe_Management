from typing import Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(
    db: Session,
    page: int = 1,
    limit: int = 10,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    in_stock_only: bool = False,
) -> tuple[list[Product], int]:
    query = db.query(Product)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if in_stock_only:
        query = query.filter(Product.stock > 0)

    total = query.count()
    total_pages = max(1, (total + limit - 1) // limit)

    products = (
        query.options(joinedload(Product.category))
        .order_by(Product.name)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return products, total, total_pages


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        category_id=data.category_id,
        image_url=data.image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
