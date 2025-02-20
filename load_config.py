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