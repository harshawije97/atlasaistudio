from src.utils.data_model import MessageModel
from src.events.event_embeddings import embeddings, get_index

async def chat_chain_event_handler(values: MessageModel):
    try:
        embed_values = embeddings.embed_query(values.message)
        index = get_index(index=values.metadata.get("index")) # type: ignore

        vectors = index.query(
            vector=embed_values,
            top_k=10,
            include_metadata=True,
            namespace=values.metadata.get("namespace"),
        )

        matches = vectors.get('matches', [])
        context = "\n\n".join([match['metadata'].get('text', '')
                              for match in matches])

        return context
    except Exception as e:
        return str(e)
