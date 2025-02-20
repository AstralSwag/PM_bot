from printer import get_inwork_issues_alltime
from load_config import load_config
import sys

config = load_config()

API_KEY = config.get("API_KEY")

# Получение USER_ID из аргументов командной строки
if len(sys.argv) < 2:
    print("Ошибка: USER_ID не указан.")
    sys.exit(1)

USER_ID = sys.argv[1]

get_inwork_issues_alltime(API_KEY, USER_ID)