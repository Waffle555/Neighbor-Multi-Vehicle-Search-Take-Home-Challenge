from pydantic import BaseModel

class Vehicle(BaseModel):
    length: int
    quantity: int

class VehicleFlattened(BaseModel):
    length: int
    width: int
