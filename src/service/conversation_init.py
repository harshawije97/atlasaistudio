import logging
from src.utils.base_template import base_template as base
from src.utils.data_model import NewMessageModel
from starlette.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


async def chat_event_handler(values: NewMessageModel):
    try:
        async def generate():
            # template
            template = ChatPromptTemplate.from_template(base)
            # bind into the prompt
            prompt = template.format(question=values.message)
            # get llm
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
            )
            # chunk answers into a stream
            for chunk in llm.stream(prompt):
                logging.debug(f"Received chunk: {chunk}")
                yield f"{chunk.content}"
            
        return StreamingResponse(generate(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})

    except Exception as e:
        print(e)
