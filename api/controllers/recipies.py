# controllers/recipes.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, recipe):
    db_recipe = models.Recipe(
        id=recipe.id,
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id,
        amount=recipe.amount
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    return recipe

def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    query = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    update_data = recipe.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db.commit()
    return query.first()

def delete(db: Session, recipe_id: int):
    query = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
