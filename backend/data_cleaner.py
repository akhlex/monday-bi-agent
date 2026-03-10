import pandas as pd

def normalize_sector(sector):

    if not sector:
        return "unknown"

    sector = sector.lower().strip()

    mapping = {
        "energy sector": "energy",
        "oil & gas": "energy",
        "energy & utilities": "energy"
    }

    return mapping.get(sector, sector)


def clean_dataframe(df):

    if "sector" in df.columns:
        df["sector"] = df["sector"].apply(normalize_sector)

    return df