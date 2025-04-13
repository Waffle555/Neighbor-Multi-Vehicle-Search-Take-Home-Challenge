from app.domain.helper import (
    find_cheapest_fit_listing_combo_in_listings,
    find_fit_listings_in_location,
    flaten_vehicle_list,
)
from app.schema.storage import MultiVehicleStorageSolution
from app.service.storage import StorageService
from app.schema.vehicle import Vehicle


class MultiVehicleStorageSolver:
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service

    def solve(self, vehicle_inputs: list[Vehicle]) -> list[MultiVehicleStorageSolution]:
        vehicles = flaten_vehicle_list(vehicle_inputs)
        storage_grouped_by_location = (
            self.storage_service.get_storage_grouped_by_location()
        )

        solutions = []
        for location_id, storage_listings in storage_grouped_by_location.items():
            # rotate all listings in each location to find the best fit

            listings = find_fit_listings_in_location(
                location_id, storage_listings, vehicles
            )
            cheapest_combo, total_price = find_cheapest_fit_listing_combo_in_listings(
                listings
            )
            if cheapest_combo:
                solutions.append(
                    MultiVehicleStorageSolution(
                        location_id=location_id,
                        listing_ids=[l.id for l in cheapest_combo],
                        total_price_in_cents=total_price,
                    )
                )

        solutions.sort(key=lambda x: x.total_price_in_cents)
        return solutions
