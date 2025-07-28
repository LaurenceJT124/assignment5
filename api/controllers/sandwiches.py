from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        id= sandwich.id,
        sandwich_name = sandwich.sandwich_name,
        price = sandwich.price,
        recipes = sandwich.recipes,
        order_details = sandwich.order_details
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all(db: Session):
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()

    return sandwich

def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    query = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)

    update_data = sandwich.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db.commit()
    return query.first()

def delete(db: Session, sandwich_id: int):
    query = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
