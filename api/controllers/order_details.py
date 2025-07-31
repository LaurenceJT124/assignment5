# controllers/order_details.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, order_detail):
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id,
        amount=order_detail.amount
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def read_all(db: Session):
    return db.query(models.OrderDetail).all()

def read_one(db: Session, order_detail_id: int):
    order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    return order_detail

def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    query = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    update_data = order_detail.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db.commit()
    return query.first()

def delete(db: Session, order_detail_id: int):
    query = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
