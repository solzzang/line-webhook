from flask import Flask, request
import json, hmac, hashlib, base64

app = Flask(__name__)
CHANNEL_SECRET = "e042abfbb258184b5f014609d19dc52b"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    hash = hmac.new(CHANNEL_SECRET.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode("utf-8")

    if signature != signature:
        return "Invalid signature", 403

    events = json.loads(body).get("events", [])
    for event in events:
        if event.get("type") == "message":
            user_id = event["source"]["userId"]
            text = event["message"]["text"]
            print(f"👤 userId: {user_id}, 📩 메시지: {text}")
    return "OK"