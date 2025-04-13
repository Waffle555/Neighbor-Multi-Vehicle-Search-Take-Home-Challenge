from app.db.storage.storage_listing_adapter import StorageListingAdapter
from app.schema.storage import Storage
from functools import lru_cache
from collections import defaultdict


class StorageService:
    # service layer protects the domain layer from knowing about the implementation details of the repository
    def __init__(self, repository: StorageListingAdapter):
        # normally we would use database connection here
        self.repository = repository

    def get_collection(self, offset: int = 0, limit: int = 100)->list[Storage]:
        return self.repository.get_collection(offset, limit)

    @lru_cache(maxsize=10)
    def get_storage_grouped_by_location(self)->dict[str, list[Storage]]:
        """
        key: location_id
        value: list of storage listings
        """
        storage_listings = self.get_collection(limit=10000) # could iterate over all with smaller limit
        storage_grouped_by_location = defaultdict(list)
        for storage_listing in storage_listings:
            storage_grouped_by_location[storage_listing.location_id].append(storage_listing)
        return storage_grouped_by_location

