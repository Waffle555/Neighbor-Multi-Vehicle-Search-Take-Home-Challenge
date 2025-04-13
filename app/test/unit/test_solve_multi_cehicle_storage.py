import pytest
from app.domain.multi_vehicle_storage_solver import MultiVehicleStorageSolver
from app.schema.storage import MultiVehicleStorageSolution, Storage
from app.schema.vehicle import Vehicle


class DummyStorageService:
    def get_storage_grouped_by_location(self):
        return {
            "1": [
                Storage(
                    id="1", length=15, width=15, price_in_cents=100, location_id="1"
                ),
                Storage(
                    id="2", length=20, width=20, price_in_cents=200, location_id="1"
                ),
            ],
            "2": [
                Storage(
                    id="3", length=15, width=10, price_in_cents=50, location_id="2"
                ),
                Storage(
                    id="4", length=10, width=20, price_in_cents=100, location_id="2"
                ),
            ],
            "3": [
                Storage(id="5", length=5, width=10, price_in_cents=60, location_id="3"),
                Storage(id="6", length=10, width=5, price_in_cents=40, location_id="3"),
            ],
            "4": [
                Storage(
                    id="7", length=10, width=10, price_in_cents=50, location_id="4"
                ),
                Storage(
                    id="8", length=10, width=15, price_in_cents=100, location_id="4"
                ),
            ],
        }


@pytest.fixture
def multi_vehicle_storage_solver():
    dummy_storage_service = DummyStorageService()
    return MultiVehicleStorageSolver(dummy_storage_service)


def test_solve_multi_vehicle_storage(multi_vehicle_storage_solver):
    vehicles = [
        Vehicle(length=10, quantity=1),
        Vehicle(length=10, quantity=1),
    ]
    assert multi_vehicle_storage_solver.solve(vehicles) == [
        MultiVehicleStorageSolution(
            location_id="2",
            listing_ids=["4"],
            total_price_in_cents=100,
        ),
        MultiVehicleStorageSolution(
            location_id="4",
            listing_ids=["7", "8"],
            total_price_in_cents=150,
        ),
        MultiVehicleStorageSolution(
            location_id="1",
            listing_ids=["2"],
            total_price_in_cents=200,
        ),
    ]

def test_empty_vehicle_list(multi_vehicle_storage_solver):
    vehicles = []
    assert multi_vehicle_storage_solver.solve(vehicles) == []


