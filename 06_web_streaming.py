from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from litellm import acompletion
import os

app = FastAPI()

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "06_index.html"))

@app.post("/chat")
async def chat_stream(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    async def stream_generator():
        # Await the coroutine to get the async generator
        completion = await acompletion(
            model="ollama/llama3.2",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        # Now completion is an async iterator
        async for chunk in completion:
            content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
            if content:
                yield content

    return StreamingResponse(stream_generator(), media_type="text/plain")
