import json
from datetime import datetime

BOOKING_FILE = "data/bookings.json"

BOOKING_TEMPLATE = (
    "กรุณากรอกข้อมูลจองคิวตามนี้ 💅\n\n"
    "ชื่อเล่น:\n"
    "เบอร์โทร:\n"
    "สาขา:\n"
    "วันที่:\n"
    "เวลา:\n"
    "จองช่างประจำหรือไม่:\n"
    "ชื่อช่าง:\n"
    "บริการ:\n\n"
    "ตัวอย่าง\n"
    "ชื่อเล่น: แพรว\n"
    "เบอร์โทร: 0999999999\n"
    "สาขา: ตลาดเชฟวันโก\n"
    "วันที่: 27/05/2026\n"
    "เวลา: 14:00\n"
    "จองช่างประจำหรือไม่: จอง\n"
    "ชื่อช่าง: มิ้น\n"
    "บริการ: ทาสีเจลมือ, เพนท์ลาย"
)

def load_bookings():
    try:
        with open(BOOKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)

    with open(BOOKING_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def get_value(text, key):
    for line in text.splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip()
    return ""

def is_time_available(branch, date, time, staff):
    bookings = load_bookings()

    for booking in bookings:
        if (
            booking.get("branch") == branch
            and booking.get("date") == date
            and booking.get("time") == time
        ):
            if staff == "" or staff == "ไม่จอง" or staff == "ไม่จองช่างประจำ":
                return False

            if booking.get("staff") == staff:
                return False

    return True

def start_booking(user_id=None):
    return BOOKING_TEMPLATE

def handle_booking(user_id, text):
    if "ชื่อเล่น:" not in text or "เบอร์โทร:" not in text:
        return None

    booking = {
        "nickname": get_value(text, "ชื่อเล่น"),
        "phone": get_value(text, "เบอร์โทร"),
        "branch": get_value(text, "สาขา"),
        "date": get_value(text, "วันที่"),
        "time": get_value(text, "เวลา"),
        "staff_choice": get_value(text, "จองช่างประจำหรือไม่"),
        "staff": get_value(text, "ชื่อช่าง"),
        "service": get_value(text, "บริการ"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    required_fields = ["nickname", "phone", "branch", "date", "time", "service"]
    for field in required_fields:
        if not booking[field]:
            return "ข้อมูลยังไม่ครบค่ะ กรุณากรอกใหม่ให้ครบตามแบบฟอร์มค่ะ 💅"

    if booking["staff_choice"] in ["ไม่จอง", "ไม่จองช่างประจำ", "ไม่"]:
        booking["staff"] = "ไม่จองช่างประจำ"

    available = is_time_available(
        booking["branch"],
        booking["date"],
        booking["time"],
        booking["staff"]
    )

    if not available:
        return (
            "ขออภัยค่ะ เวลานี้คิวเต็มแล้ว ❌\n"
            "กรุณาเลือกวันหรือเวลาใหม่ แล้วส่งแบบฟอร์มจองคิวมาอีกครั้งค่ะ"
        )

    save_booking(booking)

    return (
        "จองคิวเรียบร้อยค่ะ ✅\n\n"
        f"ชื่อเล่น: {booking['nickname']}\n"
        f"เบอร์โทร: {booking['phone']}\n"
        f"สาขา: {booking['branch']}\n"
        f"วันที่: {booking['date']}\n"
        f"เวลา: {booking['time']}\n"
        f"ช่าง: {booking['staff']}\n"
        f"บริการ: {booking['service']}"
    )