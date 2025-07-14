import logging
from typing import Any, List, Dict
from fastapi import HTTPException
from src.events.event_embeddings import get_pinecone_client


def get_all_vector_indexes() -> Any:
    try:
        pc = get_pinecone_client()
        indexes_list = pc.list_indexes()

        serialized_indexes = [
            {
                "name": index.name,
                "dimension": index.dimension,
                "metric": index.metric,
                "status": {
                    "ready": index.status.ready,
                    "state": index.status.state
                }
            }
            for index in indexes_list.indexes
        ]

        return serialized_indexes
    except Exception as e:
        logging.exception("Error in document event handler")
        raise HTTPException(status_code=500, detail=str(e))
