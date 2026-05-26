from flask import Flask, request
from dotenv import load_dotenv
import os

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "Nail Salon Bot Running!"

@app.route("/callback", methods=["POST"])
def callback():
    print("LINE WEBHOOK RECEIVED")
    print(request.get_data(as_text=True))

    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("ERROR:", e)

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("MESSAGE:", event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="บอทตอบแล้วค่ะ 💅")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
