from pydantic import BaseModel

class SalesTotalResponse(BaseModel):
    total: int

class SalesTopProductsResponse(BaseModel):
    name: str
    sold_amount: int

