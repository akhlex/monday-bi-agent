import re

SECTORS = [
    "mining",
    "powerline",
    "solar",
    "infrastructure",
    "railway",
    "oil",
    "energy"
]

METRICS = {
    "pipeline": ["pipeline", "deals", "sales"],
    "projects": ["projects", "work orders"],
    "billed": ["billed", "billing"],
    "collected": ["collected", "collections"],
    "receivable": ["receivable", "pending payment"],
    "conversion": ["conversion", "converted"]
}

TIME_KEYWORDS = {
    "quarter": ["quarter", "this quarter"],
    "month": ["month", "this month"],
    "year": ["year", "this year"]
}

def is_leadership_query(query):

    query = query.lower()

    keywords = [
        "leadership update",
        "executive summary",
        "company update",
        "board update",
        "status summary"
    ]

    return any(word in query for word in keywords)


def interpret_query(query):

    query = query.lower()

    result = {
        "sector": None,
        "metric": None,
        "timeframe": None
    }

    # Detect sector
    for sector in SECTORS:
        if sector in query:
            result["sector"] = sector

    # Detect metric
    for metric, keywords in METRICS.items():
        for word in keywords:
            if word in query:
                result["metric"] = metric

    # Detect timeframe
    for timeframe, words in TIME_KEYWORDS.items():
        for word in words:
            if word in query:
                result["timeframe"] = timeframe

    return result