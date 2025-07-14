from typing import Any
from langchain_openai import OpenAIEmbeddings
from os import getenv
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone.grpc import PineconeGRPC

load_dotenv()

embeddings = OpenAIEmbeddings(api_key=getenv(
    "OPENAI_API_KEY"),  # type: ignore
    model="text-embedding-3-small",
)

# pinecone client


def get_pinecone_client() -> Any:
    pc = PineconeGRPC(api_key=getenv("PINECONE_API_KEY"))
    return pc

# get index
def get_index(index: str) -> Any:
    db = Pinecone(api_key=getenv("PINECONE_API_KEY"))
    return db.Index(name=index)
