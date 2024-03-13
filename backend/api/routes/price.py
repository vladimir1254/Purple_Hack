from enum import Enum
from typing import Any
from http import HTTPStatus
import io
import logging

from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from models import PriceRequest, PriceResponse

from api.exceptions import bad_data
from repositories import BaseRepository, BasePrices, DiscountPrices, DiscountPriceRepository, BasePriceRepository

from services import find_all_parent, category_tree, location_tree

router = APIRouter()
logger = logging.getLogger()


users = {
	2100: {156, 278},
	2200: {168, 290, 412},
	2300: {180},
	2400: {192, 314, 436, 158},
	2500: {204, 326, 148, 370, 592},
	2600: {216},
	2700: {228, 350, 472, 194},
	2800: {},
	2900: {240, 362, 484, 206, 428},
	3000: {252, 374},
	3100: {264, 386, 508, 230},
	3200: {276, 398},
	3300: {288, 410, 532, 254},
	3400: {300, 422, 544, 166},
	3500: {312, 434},
	3600: {324, 446, 568, 190},
	3700: {336, 458},
	3800: {348, 470, 592, 214},
	3900: {360, 482, 604, 226},
	4000: {372, 494, 616, 238},
	4100: {384, 506, 628, 250},
	4200: {396, 518, 640, 262},
}
@router.post("/")
async def get_prices(request: PriceRequest):
    if request.user_id in users:
        for segment_id in sorted(users[request.user_id],reverse=True):
            location_parents = find_all_parent(request.location_id, location_tree)
            category_parents = find_all_parent(request.category_id, category_tree)

            help_query_location = ', '.join([str(t) for t in location_parents])
            help_query_category = ', '.join([str(t) for t in category_parents])
            query = f'''select * from purple.discount_prices where location_id in ({help_query_location}) and
            category_id in ({help_query_category}) and segment_id in ({segment_id})
            '''
            matrix = BasePriceRepository().array_query(query,segment_id)
            if matrix!={}:
                return matrix
    location_parents = find_all_parent(request.location_id, location_tree)
    category_parents = find_all_parent(request.category_id, category_tree)

    help_query_location = ', '.join([str(t) for t in location_parents])
    help_query_category = ', '.join([str(t) for t in category_parents])
    query = f'''select * from purple.base_prices where location_id in ({help_query_location}) and
    category_id in ({help_query_category})
    '''
    matrix = BasePriceRepository().array_query(query)    
    return matrix
