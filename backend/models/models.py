from pydantic import BaseModel
from typing import List


class PriceRequest(BaseModel):
    location_id: int
    category_id: int
    user_id: int


class PriceResponse(BaseModel):
    price: int
    location_id: int
    category_id: int
    matrix_id: int
    user_segment_id: int


class MatrixRequest(BaseModel):
    location_id: int
    category_id: int
    price: float


class DeletePrice(BaseModel):
    location_id: int
    category_id: int


class MatrixResponse(BaseModel):
    location_id: int
    category_id: int
    price: int


class PaginationResponse(BaseModel):
    total: int
    limit: int
    offset: str = None
    last_page: int
    next_page_link: str = None
    data: List = []


class OkResponse(BaseModel):
    result: str
