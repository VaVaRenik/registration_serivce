from datetime import datetime
from pydantic import BaseModel, Field


class RegistrationBase(BaseModel):
    username: str
    place: str
    start_time: datetime
    end_time: datetime


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationRead(RegistrationBase):
    id: int

    class Config:
        orm_mode = True
