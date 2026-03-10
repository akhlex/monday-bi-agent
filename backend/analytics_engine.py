import pandas as pd

def normalize_column(name):

    if not name:
        return None

    return (
        name.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )

def process_deals(raw_items):

    rows = []

    for item in raw_items:

        row = {"deal_name": item["name"]}

        for col in item["column_values"]:

            title = col.get("column", {}).get("title")
            value = col.get("text")

            col_name = normalize_column(title)

            if col_name:
                row[col_name] = value

        rows.append(row)

    df = pd.DataFrame(rows)

    print("DEALS DF COLUMNS:", df.columns)

    # Deal value
    if "masked_deal_value" in df.columns:
        df["masked_deal_value"] = pd.to_numeric(df["masked_deal_value"], errors="coerce")
        df.rename(columns={"masked_deal_value": "deal_value"}, inplace=True)
    else:
        df["deal_value"] = 0

    # Probability
    if "closure_probability" in df.columns:
        df["closure_probability"] = pd.to_numeric(df["closure_probability"], errors="coerce")
        df.rename(columns={"closure_probability": "probability"}, inplace=True)
    else:
        df["probability"] = 0

    # Sector
    if "sector_service" in df.columns:
        df.rename(columns={"sector_service": "sector"}, inplace=True)

    if "sector" in df.columns:
        df["sector"] = df["sector"].str.lower()
    else:
        df["sector"] = "unknown"

    # Stage
    if "deal_stage" in df.columns:
        df.rename(columns={"deal_stage": "stage"}, inplace=True)
    else:
        df["stage"] = "unknown"

    # Close date
    if "tentative_close_date" in df.columns:
        df.rename(columns={"tentative_close_date": "close_date"}, inplace=True)

    return df

def process_work_orders(raw_items):

    rows = []

    for item in raw_items:

        row = {"deal_name": item["name"]}

        for col in item["column_values"]:

            title = col.get("column", {}).get("title")
            value = col.get("text")

            col_name = normalize_column(title)

            if col_name:
                row[col_name] = value

        rows.append(row)

    df = pd.DataFrame(rows)

    print("WORK DF COLUMNS:", df.columns)

    # Normalize sector
    if "sector" in df.columns:
        df["sector"] = df["sector"].str.lower()
    else:
        df["sector"] = "unknown"

    # Numeric columns
    numeric_map = {
        "amount_excl_gst": "project_value",
        "billed_value": "billed_value",
        "collected_amount": "collected_value",
        "amount_receivable": "receivable"
    }

    for source, target in numeric_map.items():

        if source in df.columns:

            df[source] = pd.to_numeric(df[source], errors="coerce")
            df.rename(columns={source: target}, inplace=True)

        else:
            df[target] = 0

    return df

def deals_summary(df):

    total_pipeline = df["deal_value"].sum()

    weighted_pipeline = (df["deal_value"] * df["probability"] / 100).sum()

    sector_breakdown = (
        df.groupby("sector")["deal_value"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    stage_distribution = (
        df.groupby("stage")
        .size()
        .to_dict()
    )

    return {
        "total_pipeline": total_pipeline,
        "weighted_pipeline": weighted_pipeline,
        "sector_pipeline": sector_breakdown,
        "stage_distribution": stage_distribution,
        "total_deals": len(df)
    }

def deals_this_quarter(df):

    df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")

    today = pd.Timestamp.today()

    quarter = (today.month - 1) // 3 + 1

    quarter_deals = df[df["close_date"].dt.quarter == quarter]

    return {
        "count": len(quarter_deals),
        "value": quarter_deals["deal_value"].sum()
    }

def work_order_summary(df):

    total_projects = len(df)

    total_project_value = df["project_value"].sum()

    billed = df["billed_value"].sum()

    collected = df["collected_value"].sum()

    receivable = df["receivable"].sum()

    sector_projects = (
        df.groupby("sector")
        .size()
        .sort_values(ascending=False)
        .to_dict()
    )

    return {
        "total_projects": total_projects,
        "total_project_value": total_project_value,
        "billed": billed,
        "collected": collected,
        "receivable": receivable,
        "sector_projects": sector_projects
    }

def conversion_metrics(deals_df, work_df):

    deals = set(deals_df["deal_name"])

    projects = set(work_df["deal_name"])

    converted = deals.intersection(projects)

    conversion_rate = len(converted) / len(deals) if deals else 0

    return {
        "total_deals": len(deals),
        "converted_projects": len(converted),
        "conversion_rate": conversion_rate
    }

def data_quality_report(deals_df, work_df):

    issues = []

    if deals_df["deal_value"].isna().sum() > 0:
        issues.append("Some deals have missing values")

    if deals_df["sector"].isna().sum() > 0:
        issues.append("Some deals missing sector information")

    if work_df["receivable"].isna().sum() > 0:
        issues.append("Some work orders missing receivable values")

    return issues

def filter_sector(df, sector):

    if sector is None:
        return df

    return df[df["sector"].str.contains(sector, na=False)]

def leadership_metrics(deals_df, work_df):

    deals = deals_summary(deals_df)
    quarter = deals_this_quarter(deals_df)
    work = work_order_summary(work_df)
    conversion = conversion_metrics(deals_df, work_df)

    return {
        "pipeline_value": deals["total_pipeline"],
        "weighted_pipeline": deals["weighted_pipeline"],
        "sector_pipeline": deals["sector_pipeline"],
        "deals_closing_quarter": quarter,
        "projects": work["total_projects"],
        "billed": work["billed"],
        "collected": work["collected"],
        "receivable": work["receivable"],
        "conversion_rate": conversion["conversion_rate"],
        "converted_projects": conversion["converted_projects"]
    }

def build_metrics(deals_df, work_df):

    deals = deals_summary(deals_df)
    quarter = deals_this_quarter(deals_df)
    work = work_order_summary(work_df)
    conversion = conversion_metrics(deals_df, work_df)

    metrics = {
        "pipeline": {
            "total_value": float(deals["total_pipeline"]),
            "weighted_pipeline": float(deals["weighted_pipeline"]),
            "total_deals": int(deals["total_deals"])
        },

        "sector_pipeline": deals["sector_pipeline"],

        "quarter_pipeline": {
            "count": int(quarter["count"]),
            "value": float(quarter["value"])
        },

        "operations": {
            "projects": int(work["total_projects"]),
            "project_value": float(work["total_project_value"]),
            "billed": float(work["billed"]),
            "collected": float(work["collected"]),
            "receivable": float(work["receivable"])
        },

        "conversion": {
            "converted_projects": int(conversion["converted_projects"]),
            "conversion_rate": float(conversion["conversion_rate"])
        }
    }

    return metrics