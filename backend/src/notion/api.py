import requests
from config_reader import config
from pprint import pprint

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

notion_api_key = config.notion_api_key.get_secret_value()
database_id = config.notion_db_id.get_secret_value()

base_url = 'https://api.notion.com/v1'

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def format_props(data):
    transformed = {}
    
    for key, value in data.items():
        if value['type'] == 'select':
            options = [option['name'] for option in value['select']['options']]
            transformed[key] = {'type': 'select', 'options': options}
        else:
            transformed[key] = {'type': value['type']}
    
    return transformed


def get_db_props():
    url = f"{base_url}/databases/{database_id}"
    response = requests.get(url, headers=headers)
    props = format_props(response.json()['properties'])
    return props


def get_buttons(property):
    options = get_db_props()[property]['options']
    buttons = [
        [KeyboardButton(text=options[i]), KeyboardButton(text=options[i+1])]
        if i + 1 < len(options) else [KeyboardButton(text=options[i])]
        for i in range(0, len(options), 2)
    ]
    return buttons


# TODO: Implement the create_db_record function
def create_db_record(properties):
    url = f"{base_url}/pages"
    data = {
        "parent": {
            "database_id": database_id
        },
        "properties": properties
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
