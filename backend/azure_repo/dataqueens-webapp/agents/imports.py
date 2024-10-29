import os
from dotenv import load_dotenv

load_dotenv(override=True)

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
EMBEDDING_DEPLOYMENT_NAME=os.getenv('EMBEDDING_DEPLOYMENT_NAME')