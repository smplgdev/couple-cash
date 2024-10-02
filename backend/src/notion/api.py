import requests

from config_reader import config
from schemas import ExpenseBase

NOTION_API_KEY = config.notion_api_key.get_secret_value()
DATABASE_ID = config.notion_db_id.get_secret_value()

NOTION_API_BASE_URL = 'https://api.notion.com/v1'

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def format_props(data: dict) -> dict:
    transformed = {}
    
    for key, value in data.items():
        if value['type'] == 'select':
            options = [option['name'] for option in value['select']['options']]
            transformed[key] = {'type': 'select', 'options': options}
        else:
            transformed[key] = {'type': value['type']}
    
    return transformed


def get_db_props() -> dict:
    url = f"{NOTION_API_BASE_URL}/databases/{DATABASE_ID}"
    response = requests.get(url, headers=headers)
    props = format_props(response.json()['properties'])
    return props


def create_notion_db_record(expense: ExpenseBase, purchaser_name: str) -> dict:
    url = f"{NOTION_API_BASE_URL}/pages"
    properties = {
        "Title": {
            "title": [
                {
                    "text": {
                        "content": expense.comment
                    }
                }
            ]
        },
        "Type of expenses": {
            "select": {
                "name": expense.payment_type  # "Split the bill" | | "Payed for my partner" | | "Payed for myself"
            }
        },
        "Cost": {
            "number": expense.amount
        },
        "Category": {
            "select": {
                "name": expense.category
            }
        },
        "Wallet": {
            "select": {
                "name": purchaser_name
            }
        }
    }
    payload = {
        "parent": {
            "database_id": DATABASE_ID
        },
        "properties": properties
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
