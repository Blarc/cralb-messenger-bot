from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import crud, schemas
from app.dependencies import get_db

router = APIRouter(
    prefix='/notes',
    tags=['notes']
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes
