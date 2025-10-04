se# server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import uvicorn

app = FastAPI()

# CORS falls nötig
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

CEREBRAS_KEY = os.getenv("CEREBRAS_KEY")  # In Koyeb als ENV Variable setzen
CEREBRAS_URL = "https://api.cerebras.ai/v1/chat/completions"

@app.post("/")
async def proxy(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {CEREBRAS_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "cerebras-llama3.1-8b",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(CEREBRAS_URL, json=body, headers=headers)
        res_json = response.json()

    return {"reply": res_json.get("choices", [{}])[0].get("message", {}).get("content", "")}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
