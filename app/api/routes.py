from fastapi import APIRouter
from app.db.storage.storage_listing_adapter import StorageListingAdapter
from app.domain.multi_vehicle_storage_solver import MultiVehicleStorageSolver
from app.schema.storage import MultiVehicleStorageSolution
from app.schema.vehicle import Vehicle
from app.service.storage import StorageService


router = APIRouter()


@router.post("/")
def solve_multi_vehicle_storage(
    vehicles: list[Vehicle],
) -> list[MultiVehicleStorageSolution]:
    storage_listing_adapter = StorageListingAdapter()
    storage_service = StorageService(storage_listing_adapter)
    multi_vehicle_storage_solver = MultiVehicleStorageSolver(storage_service)
    return multi_vehicle_storage_solver.solve(vehicles)


@router.get("/health")
async def health():
    return {"status": "ok"}
