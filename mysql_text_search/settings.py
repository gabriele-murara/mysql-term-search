import os
from dotenv import load_dotenv

from mysql_text_search.classes.env_utility import EnvUtility
from mysql_text_search.classes.match_types import MatchTypes

load_dotenv(override=False)

DB_NAME = os.getenv('DB_NAME', None)
DB_HOST = os.getenv('DB_HOST', "127.0.0.1")
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', None)
DB_PORT = os.getenv('DB_PORT', 3306)

CASE_INSENSITIVE_SEARCH = EnvUtility.to_boolean(
    os.getenv('CASE_INSENSITIVE_SEARCH', False)
)

MATCH_TYPE = os.getenv('CASE_INSENSITIVE_SEARCH', MatchTypes.EXACT)
