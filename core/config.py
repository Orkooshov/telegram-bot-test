from os import environ
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

API_TOKEN = environ['api_token']

RESOURCES_FOLDER = Path(__file__).parent.parent / 'resources'

class PollCfg:
    max_columns = 3

class DatabaseConfig:
    echo = False
    pool_size = 10
    connection_str = environ['db_connection']
