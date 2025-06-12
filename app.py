from flask import Flask, request
import json, hmac, hashlib, base64
import threading
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)
CHANNEL_SECRET = "e042abfbb258184b5f014609d19dc52b"
ACCESS_TOKEN = "qW8jaVO+EKprbz/y6bPwMAcWhGLCgTS822GZGtJ3vjZsmEvH/+tPRP0BWTWktTDnuWjyfjmltnt86SdxSiZIsXdNwPVwjYRVLOz+UqWVoPBzZYMSeCpwErR7Urfk+szctzz01Tw6lxpeUOU88LvH1wdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(ACCESS_TOKEN)

def handle_event(event):
    try:
        user_id = event["source"]["userId"]
        text = event["message"]["text"]

        if "타슈" in text:
            reply = "🚲 집 앞 타슈 자전거는 3대 남았습니다! (예시)"
        else:
            reply = f"'{text}' 라고 하셨군요!"

        line_bot_api.reply_message(
            event["replyToken"],
            TextSendMessage(text=reply)
        )
    except Exception as e:
        print("❌ 처리 중 오류:", e)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    hash = hmac.new(CHANNEL_SECRET.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode("utf-8")

    if signature != computed_signature:
        return "Invalid signature", 403

    events = json.loads(body).get("events", [])
    for event in events:
        if event.get("type") == "message":
            threading.Thread(target=handle_event, args=(event,)).start()

    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
