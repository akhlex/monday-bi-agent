import pandas as pd

def pipeline_value(df):

    return df["value"].sum()


def deals_by_sector(df):

    return df.groupby("sector")["value"].sum().to_dict()


def deals_this_quarter(df):

    df["expected_close"] = pd.to_datetime(df["expected_close"])

    today = pd.Timestamp.today()

    quarter = (today.month - 1) // 3 + 1

    return df[df["expected_close"].dt.quarter == quarter]