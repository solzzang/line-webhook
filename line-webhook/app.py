from flask import Flask, request
import json
import hmac
import hashlib
import base64

app = Flask(__name__)

# 실제 Channel Secret 으로 변경하세요
CHANNEL_SECRET = "e042abfbb258184b5f014609d19dc52b"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    # 서명 검증
    hash = hmac.new(CHANNEL_SECRET.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode("utf-8")

    if signature != computed_signature:
        return "Invalid signature", 403

    events = json.loads(body).get("events", [])
    for event in events:
        if event.get("type") == "message":
            user_id = event["source"]["userId"]
            text = event["message"]["text"]
            print(f"👤 userId: {user_id}, 📩 메시지: {text}")
    return "OK"

if __name__ == "__main__":
    # Render 같은 클라우드에선 반드시 0.0.0.0으로 호스트 설정 필요
    app.run(host="0.0.0.0", port=10000)
