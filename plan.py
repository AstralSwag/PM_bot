from printer import get_inwork_issues_alltime
from load_config import load_config

config = load_config()

API_KEY = config.get("API_KEY")
USER_ID = config.get("USER_ID")

get_inwork_issues_alltime(API_KEY, USER_ID)