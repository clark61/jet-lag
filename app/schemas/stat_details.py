from pydantic import BaseModel

class StatsBase(BaseModel):
    monthly_data: list
    summary: float
    unit: str
    summaryType: str

class StatsResponse(StatsBase):
    class Config:
        orm_mode = True