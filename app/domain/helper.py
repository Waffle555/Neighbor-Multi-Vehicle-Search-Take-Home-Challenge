from app.schema.vehicle import Vehicle, VehicleFlattened
from app.schema.storage import Storage
from itertools import combinations

def flaten_vehicle_list(
    vehicles: list[Vehicle], width: int = 10
) -> list[VehicleFlattened]:
    """
    Flatten a list of vehicles with quantities into individual vehicle objects.
    """
    flattened = []
    for vehicle in vehicles:
        for _ in range(vehicle.quantity):
            flattened.append(VehicleFlattened(length=vehicle.length, width=width))
    return flattened


def can_fit(vehicle_length: int, vehicle_width: int, listing: Storage) -> int:
    rows = listing.length // vehicle_length
    cols = listing.width // vehicle_width
    return rows * cols

def total_area_check(combo: list[Storage], vehicles: list[VehicleFlattened]) -> bool:
    total_vehicle_area = sum(v.length * v.width for v in vehicles)
    total_listing_area = sum(l.length * l.width for l in combo)
    return total_listing_area >= total_vehicle_area

def add_rotated_listings(original_listings: list[Storage]) -> list[Storage]:
    return original_listings + [
        Storage(
            id=listing.id,
            length=listing.width,
            width=listing.length,
            price_in_cents=listing.price_in_cents,
            location_id=listing.location_id,
        )
        for listing in original_listings
        if listing.length != listing.width
    ]

def variable_size_bin_packing(items, bin_capacities):

    items = sorted(items, reverse=True)
    
    bins = [[] for _ in bin_capacities]
    bin_remaining = bin_capacities[:]

    for item in items:
        placed = False
        for i, remaining in enumerate(bin_remaining):
            if item <= remaining:
                bins[i].append(item)
                bin_remaining[i] -= item
                placed = True
                break
        if not placed:
            raise ValueError(f"Item {item} doesn't fit in any available bin")
    
    return bins, bin_remaining

def find_fit_using_bin_packing(
    listings: list[Storage], vehicles: list[VehicleFlattened]
) -> bool:
    if not vehicles:
        return False
    vehicles_lengths = [v.length for v in vehicles]

    # convert listings to varibale size bins
    variable_size_bins = []
    for listing in listings:
        row_count = listing.length // vehicles[0].width # assume all vehicles have the same width
        for _ in range(row_count):
            variable_size_bins.append(listing.length)


    try:
        variable_size_bin_packing(vehicles_lengths, variable_size_bins)
    except ValueError as e:
        return False

    return True

def has_dup_listing_id_in_combo(combo: list[Storage]) -> bool:
    return len(combo) != len(set(c.id for c in combo))

def find_fit_listings_in_location(
    location_id: str, original_listings: list[Storage], vehicles: list[VehicleFlattened]
) -> list[Storage]:
    """because all vehicles have the same width,
    we can treat the problem as a 1D problem after coverting each listing to multiple bins
    """
    # duplicate listings to include 90 degree rotations for listings that have different length and width
    listings = add_rotated_listings(original_listings)

    result = []
    for amt in range(1, len(listings) + 1):
        for combo in combinations(listings, amt):
            if not total_area_check(combo, vehicles) or has_dup_listing_id_in_combo(combo):
                continue
            
            if find_fit_using_bin_packing(combo, vehicles):
                result.append(combo)
    
    return result

def find_cheapest_fit_listing_combo_in_listings(
    listings: list[list[Storage]]
) -> tuple[list[Storage], int]:
    min_price = float('inf')
    min_combo = None

    for combo in listings:
        total_price = sum(l.price_in_cents for l in combo)
        if total_price < min_price:
            min_price = total_price
            min_combo = combo

    return min_combo, min_price

