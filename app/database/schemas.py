from typing import List, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    value: Optional[str] = None
    category: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_email: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    messenger_id: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    notes: List[Note] = []

    class Config:
        orm_mode = True
