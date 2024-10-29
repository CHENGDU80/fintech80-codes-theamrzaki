from agents.imports import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, EMBEDDING_DEPLOYMENT_NAME
from langchain_openai import AzureOpenAIEmbeddings


EMBEDDING_MODEL = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version='2024-02-01',
    azure_deployment=EMBEDDING_DEPLOYMENT_NAME
)


def embed(prompt: str) -> dict:
    ai_msg = EMBEDDING_MODEL.embed_query(prompt)
    return ai_msg