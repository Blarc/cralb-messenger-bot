from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, messenger_id=user.messenger_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_user_note(db: Session, note: schemas.NoteCreate, owner_email: str):
    db_note = models.Note(**note.dict(), owner_email=owner_email)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
