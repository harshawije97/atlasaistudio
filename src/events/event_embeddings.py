from typing import Any
from langchain_openai import OpenAIEmbeddings
from os import getenv
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

embeddings = OpenAIEmbeddings(api_key=getenv(
    "OPENAI_API_KEY"),  # type: ignore
    model="text-embedding-3-small",
)

# get index
def get_index(index: str) -> Any:
    pc = Pinecone(api_key=getenv("PINECONE_API_KEY"))
    return pc.Index(name=index)