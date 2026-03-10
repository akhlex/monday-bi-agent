import time

CACHE = {
    "deals": None,
    "work_orders": None,
    "timestamp": 0
}

CACHE_TTL = 30  # seconds


def get_cache():

    now = time.time()

    if now - CACHE["timestamp"] < CACHE_TTL:
        return CACHE["deals"], CACHE["work_orders"]

    return None, None


def set_cache(deals, work_orders):

    CACHE["deals"] = deals
    CACHE["work_orders"] = work_orders
    CACHE["timestamp"] = time.time()