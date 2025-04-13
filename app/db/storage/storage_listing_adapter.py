import json
from app.schema.storage import Storage

class StorageListingAdapter:
    def __init__(self):
        pass

    def get_collection(self, offset: int = 0, limit: int = 100) -> list[Storage]:
        with open("app/db/storage/listings.json", "r") as f:
            data = json.load(f)
        paginated_data = data[offset:offset+limit]
        return [Storage(**item) for item in paginated_data]

