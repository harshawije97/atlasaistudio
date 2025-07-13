from starlette.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.data_model import MessageModel
from src.events.event_embeddings import embeddings, get_index
from langchain_core.prompts import ChatPromptTemplate
from src.utils.templates.marketing_template import marketing_template
import asyncio
import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()


async def marketing_chain_event_handler(values: MessageModel):
    try:
        embed_values = embeddings.embed_query(values.message)
        index = get_index(index=values.metadata.model_dump().get(
            "index"))  # type: ignore

        vectors = index.query(
            vector=embed_values,
            top_k=10,
            include_metadata=True,
            namespace=values.metadata.model_dump().get("namespace"),
        )

        matches = vectors.get('matches', [])
        context = "\n\n".join([match['metadata'].get('text', '')
                              for match in matches])

        async def text_stream():
            template = ChatPromptTemplate.from_template(marketing_template)

            prompt = template.format(
                context=context,
                chat_history=values.chat_history,
                question=values.message
            )

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
            )  # type: ignore

            for chunk in llm.stream(prompt):
                logging.debug(f"Received chunk: {chunk}")
                await asyncio.sleep(0.1)
                yield f"{chunk.content}"
                
        return StreamingResponse(text_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
    
    except Exception as e:
        logging.exception("Error in document event handler")
        return StreamingResponse(content=iter([str(e)]), media_type="text/event-stream")
