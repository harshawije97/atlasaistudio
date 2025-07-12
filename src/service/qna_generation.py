from fastapi.responses import StreamingResponse
from langchain_anthropic import ChatAnthropic
from src.utils.data_model import MessageModel
from src.events.event_embeddings import embeddings, get_index
from langchain_core.prompts import ChatPromptTemplate
from src.utils.templates.question_builder import qna_template
from os import getenv
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()


async def chat_qna_generate_handler(values: MessageModel):
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
            template = ChatPromptTemplate.from_template(qna_template)

            prompt = template.format(
                context=context,
                chat_history=values.chat_history,
                question=values.message
            )

            llm = ChatAnthropic(
                api_key=getenv("ANTHROPIC_API_KEY"),
                model_name="claude-3-7-sonnet-20250219",
                temperature=0.7,
                streaming=True,
            )  # type: ignore

            for chunk in llm.stream(prompt):
                logging.debug(f"Received chunk: {chunk}")
                await asyncio.sleep(0.1)
                yield f"{chunk.content}"

        return StreamingResponse(text_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})

    except Exception as e:
        logging.exception("Error in document event handler")
        return StreamingResponse(content=iter([str(e)]), media_type="text/event-stream")
