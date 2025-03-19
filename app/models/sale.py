from pydantic import BaseModel

class SalesTotalResponse(BaseModel):
    name: str
    sold_value: float
    total_value: float


class SalesTopProductsResponse(BaseModel):
    name: str
    sold_amount: int
    sold_value: float

