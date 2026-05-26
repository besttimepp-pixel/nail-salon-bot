from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    ImageMessage,
    TextSendMessage,
    ImageSendMessage
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route("/")
def home():
    return "Bot is running"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


def start_booking(user_id):
    return """กรุณาส่งข้อมูลตามนี้

ชื่อเล่น:
เบอร์โทร:
สาขา:
พิมพ์หมายเลข 1 = สาขาตลาดเชฟวันโก
พิมพ์หมายเลข 2 = สาขาคลองหก
วันที่:
เวลา:
จองช่างประจำหรือไม่:
ชื่อช่าง:
บริการ:

ตัวอย่าง

ชื่อเล่น: แพรว
เบอร์โทร: 0999999999
สาขา: 1
วันที่: 27/05/2026
เวลา: 14:00
จองช่างประจำหรือไม่: จอง
ชื่อช่าง: มิ้น
บริการ: ทาสีเจลมือ, เพ้นท์ลาย
"""


def convert_branch(text):
    lines = text.strip().split("\n")

    if len(lines) >= 3:
        branch = lines[2].strip()

        if branch == "1":
            lines[2] = "สาขาตลาดเชฟวันโก"
        elif branch == "2":
            lines[2] = "สาขาคลองหก"

    return "\n".join(lines)


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
        return

    text = convert_branch(text)
    booking_reply = handle_booking(user_id, text)

    if booking_reply:
        messages = [
            TextSendMessage(
                text="""กรุณาโอนมัดจำเพื่อยืนยันคิว 💅

ยอดมัดจำ 100 บาท
กรุณาโอนภายใน 15 นาที

ธนาคาร: ทหารไทยธนชาต
เลขบัญชี: 7609901702
ชื่อบัญชี: ธิดารัตน์ บุญจันทร์"""
            ),
            ImageSendMessage(
                original_content_url="https://i.postimg.cc/hvZgXJJ3/att-Ep-Sv-Klk-Yj-kty5NR45By-GTs-LD-0I-Lo-FVm-Qx-RXR8s-XM.jpg",
                preview_image_url="https://i.postimg.cc/hvZgXJJ3/att-Ep-Sv-Klk-Yj-kty5NR45By-GTs-LD-0I-Lo-FVm-Qx-RXR8s-XM.jpg"
            ),
            ImageSendMessage(
                original_content_url="https://i.postimg.cc/dQjcpCDn/line-oa-chat-260222-171329.jpg",
                preview_image_url="https://i.postimg.cc/dQjcpCDn/line-oa-chat-260222-171329.jpg"
            ),
            TextSendMessage(
                text="หลังโอนเสร็จ กรุณาส่งสลิปเพื่อยืนยันคิว 🙏"
            )
        ]

        line_bot_api.reply_message(event.reply_token, messages)

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="พิมพ์ว่า จองคิว เพื่อเริ่ม")
        )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="""ชำระมัดจำเรียบร้อยแล้วค่ะ ✅

ทางร้านยืนยันคิวให้เรียบร้อยแล้ว
ขอบคุณที่ใช้บริการ 103STUDIO 💅"""
        )
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)