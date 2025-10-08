from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CatchBase(BaseModel):
    species: str
    quantity: int
    size_cm: Optional[float] = None
    lat: float
    lon: float
    photo_url: Optional[str] = None

class CatchCreate(CatchBase):
    fisherman_id: Optional[int] = None

class Catch(CatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class FishermanBase(BaseModel):
    name: str
    phone: Optional[str] = None

class FishermanCreate(FishermanBase):
    pass

class Fisherman(FishermanBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
