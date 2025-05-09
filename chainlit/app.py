from openai import AsyncOpenAI
import chainlit as cl
import os 

api_key = os.getenv('api_key')
client = AsyncOpenAI(api_key = api_key)

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            }
        ],
    )

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append(
        {
            "role": "user", 
            "content": message.content
        }
    )

    msg = cl.Message(content="")
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    print(message_history)
    await msg.update()
