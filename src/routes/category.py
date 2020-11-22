from typing import List

from fastapi import HTTPException, APIRouter, Query
from pydantic import BaseModel

router = APIRouter()
db = {}


class Category(BaseModel):
    name: str = Query(..., min_length=2, max_length=30)
    id: int


@router.get('/categories/{category_id}')
def get_one(category_id: int):
    try:
        category = db[str(category_id)]
    except KeyError:
        raise HTTPException(status_code=404, detail=f'Category with id "{category_id}" not found')

    return category


@router.get('/categories')
def get_all():
    return db


@router.post('/categories')
def post(categories: List[Category]):
    errors = []
    for c in categories:
        if c.name in db.values():
            errors.append(f'Category with name "{c.name}" already exists')
        if str(c.id) in db.keys():
            errors.append(f'Category with id "{c.id}" already exists')

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    for c in categories:
        db[str(c.id)] = c.name

    return categories


@router.delete('/categories/{category_id}')
def delete(category_id: int):
    try:
        del db[str(category_id)]
    except KeyError:
        raise HTTPException(status_code=404, detail=f'Category with id "{category_id}" not found')
    return f'delete category {category_id}'
