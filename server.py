# server.py
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CEREBRAS_KEY = os.getenv("CEREBRAS_KEY")  # API-Key als ENV Variable
CEREBRAS_URL = "https://api.cerebras.ai/v1/chat/completions"

# --------------------
# Health-Check Endpoint
# --------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# --------------------
# Proxy Endpoint
# --------------------
@app.route("/", methods=["POST"])
def proxy():
    data = request.get_json()
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {CEREBRAS_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "cerebras-llama3.1-8b",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(CEREBRAS_URL, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        res_json = response.json()
        reply = res_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify({"reply": reply})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

# --------------------
# Server starten
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
