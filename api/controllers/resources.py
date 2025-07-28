
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, resource):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id: int):
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    return resource

def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    query = db.query(models.Resource).filter(models.Resource.id == resource_id)
    update_data = resource.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db.commit()
    return query.first()

def delete(db: Session, resource_id: int):
    query = db.query(models.Resource).filter(models.Resource.id == resource_id)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
