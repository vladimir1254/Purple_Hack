from repositories.base_repository import BaseRepository
from repositories.base_repository import BasePrices, DiscountPrices


class BasePriceRepository(BaseRepository):

    _model = BasePrices


class DiscountPriceRepository(BaseRepository):

    _model = DiscountPrices
