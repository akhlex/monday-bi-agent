import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY")

def fetch_board(board_id):

    query = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        items_page {
          items {
            name
            column_values {
              id
              text
              value
              column {
                title
              }
            }
          }
        }
      }
    }
    """

    response = requests.post(
        "https://api.monday.com/v2",
        json={
            "query": query,
            "variables": {"board_id": board_id}
        },
        headers={"Authorization": API_KEY},
    )

    return response.json()