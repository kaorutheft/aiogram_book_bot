import json


def save_users(dictionary: dict) -> dict:
    with open('database\\database.json', 'w') as file:
        json.dump(dictionary, file, indent=4)


def change_information_in_db(dictionary: dict) -> dict:
    with open('database\\database.json', 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)
