from printer import get_inwork_issues_alltime
import json

CONFIG_PATH = './config/config.json'

def load_config():
    """Загружает конфигурацию из JSON-файла"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки конфига: {e}")
        exit()

# Загружаем конфигурацию
config = load_config()

API_KEY = config.get("API_KEY")
USER_ID = config.get("USER_ID")

get_inwork_issues_alltime(API_KEY, USER_ID)