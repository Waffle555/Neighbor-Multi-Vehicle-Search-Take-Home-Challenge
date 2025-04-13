from pydantic import BaseModel

class Storage(BaseModel):
    id: str
    location_id: str
    length: int # ft, All `length` and `width` values are multiples of 10.
    width: int # ft
    price_in_cents: int # cents

class MultiVehicleStorageSolution(BaseModel):
    location_id: str
    listing_ids: list[str]
    total_price_in_cents: int
