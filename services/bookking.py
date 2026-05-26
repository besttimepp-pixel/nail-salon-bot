import json
from datetime import datetime

BOOKING_FILE = "data/bookings.json"

user_state = {}

def start_booking(user_id):
    user_state[user_id] = {"step": "branch"}
    return "กรุณาเลือกสาขาค่ะ\n1️⃣ สาขา 1\n2️⃣ สาขา 2"

def handle_booking(user_id, text):
    state = user_state.get(user_id)

    if not state:
        return None

    if state["step"] == "branch":
        state["branch"] = text
        state["step"] = "service"
        return "เลือกบริการค่ะ\n1️⃣ ทาสีเจล\n2️⃣ ต่อเล็บ\n3️⃣ เพ้นท์เล็บ\n4️⃣ ถอดเล็บ"

    if state["step"] == "service":
        state["service"] = text
        state["step"] = "info"
        return "กรุณาส่งข้อมูลแบบนี้ค่ะ\nชื่อ:\nเบอร์:\nวันเวลา:"

    if state["step"] == "info":
        state["info"] = text
        state["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_booking(state)
        user_state.pop(user_id)

        return (
            "จองคิวเรียบร้อยค่ะ ✅\n\n"
            f"สาขา: {state['branch']}\n"
            f"บริการ: {state['service']}\n"
            f"{text}"
        )

def save_booking(booking):
    try:
        with open(BOOKING_FILE, "r", encoding="utf-8") as f:
            bookings = json.load(f)
    except:
        bookings = []

    bookings.append(booking)

    with open(BOOKING_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)