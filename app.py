from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage
)

import os

app = Flask(__name__)

# LINE TOKEN
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))


@app.route("/")
def home():
    return "Bot is running"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# ฟังก์ชันเริ่มจอง
def start_booking(user_id):
    return """กรุณาส่งข้อมูลตามนี้

ชื่อเล่น:
เบอร์โทร:
สาขา:
วันที่:
เวลา:
จองช่างประจำหรือไม่:
ชื่อช่าง:
บริการ:

ตัวอย่าง

ชื่อเล่น: แพรว
เบอร์โทร: 0999999999
สาขา: ตลาดเชฟวันโก
วันที่: 27/05/2026
เวลา: 14:00
จองช่างประจำหรือไม่: จอง
ชื่อช่าง: มิ้น
บริการ: ทาสีเจลมือ, เพ้นท์ลาย
"""


# ฟังก์ชันตรวจข้อมูล
def handle_booking(user_id, text):

    lines = text.strip().split("\n")

    if len(lines) >= 6:
        return "booking_complete"

    return None


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id
    text = event.message.text.strip()

    if text == "จองคิว":

        reply = start_booking(user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    else:

        booking_reply = handle_booking(user_id, text)

        if booking_reply:

            messages = [

                TextSendMessage(
                    text="กรุณาโอนมัดจำเพื่อยืนยันคิว 💅\nยอดมัดจำ 100 บาท\nกรุณาโอนภายใน 15 นาที"
                ),

                ImageSendMessage(
                    original_content_url="https://i.postimg.cc/HnjBsF4d/att-K4gpzl-KICLx6Zhpwnwz9PAKn3n-KYw0ZXo2x-Vu-Ypho-Xs.jpg",
                    preview_image_url="https://i.postimg.cc/HnjBsF4d/att-K4gpzl-KICLx6Zhpwnwz9PAKn3n-KYw0ZXo2x-Vu-Ypho-Xs.jpg"
                ),

                ImageSendMessage(
                    original_content_url="https://i.postimg.cc/NF0P2KtN/line-oa-chat-260222-171329.jpg",
                    preview_image_url="https://i.postimg.cc/NF0P2KtN/line-oa-chat-260222-171329.jpg"
                ),

                TextSendMessage(
                    text="หลังโอนเสร็จ กรุณาส่งสลิปเพื่อยืนยันคิว 🙏"
                )
            ]

            line_bot_api.reply_message(
                event.reply_token,
                messages
            )

        else:

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="พิมพ์ว่า จองคิว เพื่อเริ่ม"
                )
            )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)