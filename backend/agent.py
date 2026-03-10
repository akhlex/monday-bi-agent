from groq_client import ask_llm
from monday_api import fetch_board
from analytics_engine import (
    process_deals,
    process_work_orders,
    build_metrics,
    data_quality_report
)
import os
from dotenv import load_dotenv
from query_interpreter import interpret_query, is_leadership_query
from analytics_engine import filter_sector, leadership_metrics
from cache import get_cache, set_cache

load_dotenv()

DEALS_BOARD = os.getenv("DEALS_BOARD_ID")
WORK_BOARD = os.getenv("WORKORDERS_BOARD_ID")


def process_query(user_query):

    intent = interpret_query(user_query)

    cached_deals, cached_work = get_cache()

    if cached_deals is not None and cached_work is not None:

        deals_df = cached_deals
        work_df = cached_work

    else:

        deals_raw = fetch_board(DEALS_BOARD)
        work_raw = fetch_board(WORK_BOARD)

        deals_items = deals_raw["data"]["boards"][0]["items_page"]["items"]
        work_items = work_raw["data"]["boards"][0]["items_page"]["items"]

        deals_df = process_deals(deals_items)
        work_df = process_work_orders(work_items)

        set_cache(deals_df, work_df)

    
    if is_leadership_query(user_query):

        metrics = leadership_metrics(deals_df, work_df)

        prompt = f"""
        You are preparing a weekly leadership update for company executives.

        Metrics:
        {metrics}

        Write a concise executive briefing with sections:

        Sales Pipeline
        Operations
        Conversion
        Risks

        Keep it short and insightful.
        """

        return ask_llm(prompt)

    # Apply sector filtering if needed
    if intent["sector"]:
        deals_df = filter_sector(deals_df, intent["sector"])
        work_df = filter_sector(work_df, intent["sector"])

    metrics = build_metrics(deals_df, work_df)

    issues = data_quality_report(deals_df, work_df)

    issue_text = ""
    if issues:
        issue_text = "\nDATA QUALITY WARNINGS:\n" + "\n".join(issues)

    prompt = f"""
    You are a business intelligence assistant helping company founders.

    Below are computed business metrics from monday.com data.

    Metrics (JSON):
    {metrics}

    User Question:
    {user_query}

    Rules:
    - Use ONLY the provided metrics.
    - Do NOT invent numbers.
    - If data is missing, say so.
    - Provide concise executive insights.

    Answer:
    """

    answer = ask_llm(prompt)

    return answer