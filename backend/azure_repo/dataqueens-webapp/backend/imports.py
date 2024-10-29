import os
from dotenv import load_dotenv

load_dotenv(override=True)

SEARCH_SERVICE_NAME=os.getenv('SEARCH_SERVICE_NAME')
SEARCH_INDEX_NAME=os.getenv('SEARCH_INDEX_NAME')
SEARCH_ADMIN_KEY=os.getenv('SEARCH_ADMIN_KEY')
SEARCH_ENDPOINT=os.getenv('SEARCH_ENDPOINT')
