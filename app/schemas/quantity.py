from pydantic import BaseModel

class QuantityBase(BaseModel):
    name: str
    param: str
    unit: str
    decimal_places: int
    summaryType: str

class QuantityResponse(QuantityBase):
    class Config:
        orm_mode = True 