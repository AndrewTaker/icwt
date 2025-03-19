from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    category_id: int


class ProductUpdate(BaseModel):
    id: int
    name: str
    category_id: int
