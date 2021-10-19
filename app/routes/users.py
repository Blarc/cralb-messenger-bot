from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import crud, schemas
from app.dependencies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users']
    # dependencies=[],
    # responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get('/{email}', response_model=schemas.User)
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post('/{email}/notes/', response_model=schemas.Note)
def create_note_for_user(
        email: str, note: schemas.NoteCreate, db: Session = Depends(get_db)
):
    return crud.create_user_note(db=db, note=note, owner_email=email)
