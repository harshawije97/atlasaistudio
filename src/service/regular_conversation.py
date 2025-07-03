import asyncio
import logging
from langchain_openai import ChatOpenAI
from src.utils.data_model import MessageModel
from src.events.event_embeddings import embeddings, get_index
from langchain_core.prompts import ChatPromptTemplate
from src.utils.templates.regular import regular_template
from starlette.responses import StreamingResponse
from os import getenv
from dotenv import load_dotenv

load_dotenv()


async def chat_chain_event_handler(values: MessageModel):
    try:
        embed_values = embeddings.embed_query(values.message)
        index = get_index(index=values.metadata.get("index"))  # type: ignore

        vectors = index.query(
            vector=embed_values,
            top_k=10,
            include_metadata=True,
            namespace=values.metadata.get("namespace"),
        )

        matches = vectors.get('matches', [])
        context = "\n\n".join([match['metadata'].get('text', '')
                              for match in matches])

        async def text_stream():
            template = ChatPromptTemplate.from_template(regular_template)

            prompt = template.format(
                context=context,
                chat_history=values.chat_history,
                question=values.message
            )

            llm = ChatOpenAI(
                api_key=getenv("OPENAI_API_KEY"), # type: ignore
                model="gpt-4o-mini-2024-07-18",
                temperature=0.7,
                streaming=True
            )

            for chunk in llm.stream(prompt):
                logging.debug(f"Received chunk: {chunk}")
                await asyncio.sleep(0.1)
                yield f"{chunk.content}"

        return StreamingResponse(text_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})

    except Exception as e:
        return str(e)
