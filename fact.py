from printer import get_done_today_issues
from load_config import load_config

config = load_config()

API_KEY = config.get("API_KEY")
USER_ID = config.get("USER_ID")

get_done_today_issues(API_KEY,USER_ID)