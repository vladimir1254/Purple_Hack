from enum import Enum
from typing import Any
from http import HTTPStatus
import io

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models import MatrixRequest, DeletePrice, PriceResponse

from repositories import BaseRepository, BasePrices, DiscountPrices, DiscountPriceRepository, BasePriceRepository

from api.exceptions import bad_data

router = APIRouter()


@router.post("/add_price")
async def insert(request: MatrixRequest):
    query = f'''
        INSERT INTO purple.base_prices (location_id, category_id, price, created) 
        values  ({request.location_id}, {request.category_id}, {request.price}, toTimestamp(now()));
        '''
    print('INSERT', query)
    BasePriceRepository().execute(query)

    return 200


@router.delete("/delete_price")
async def delete(request: DeletePrice):
    print('delte', request)
    query = f'''DELETE FROM purple.base_prices 
            WHERE location_id = {request.location_id} AND category_id = {request.category_id}'''

    BasePriceRepository().execute(query)

    return 200
