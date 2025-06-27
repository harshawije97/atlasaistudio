from langchain_openai import OpenAIEmbeddings
from os import getenv
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(api_key=getenv(
    "OPENAI_API_KEY"),  # type: ignore
    model="text-embedding-3-small",
)
