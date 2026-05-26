import json
from datetime import datetime

BOOKING_FILE = "data/bookings.json"

user_state = {}

SERVICES = (
    "กรุณาเลือกบริการโดยพิมพ์เป็นตัวเลข\n"
    "ตัวอย่าง: 1,4,5\n\n"
    "1️⃣ ทาสีเจลมือ\n"
    "2️⃣ ทาสีเจลเท้า\n"
    "3️⃣ ทาสีเจลมือเท้า\n"
    "4️⃣ ต่อเล็บ\n"
    "5️⃣ ล้างสีเจล\n"
    "6️⃣ ถอด PVC\n"
    "7️⃣ เพนท์ลาย\n"
    "8️⃣ อื่นๆ ระบุหน้าร้าน"
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

def is_time_available(branch, date, time, staff):
    bookings = load_bookings()

    for booking in bookings:
        same_branch = booking.get("branch") == branch
        same_date = booking.get("date") == date
        same_time = booking.get("time") == time

        if staff == "ไม่จองช่างประจำ":
            if same_branch and same_date and same_time:
                return False
        else:
            same_staff = booking.get("staff") == staff
            if same_branch and same_date and same_time and same_staff:
                return False

    return True

def start_booking(user_id):
    user_state[user_id] = {"step": "nickname"}
    return "กรุณาแจ้งชื่อเล่นค่ะ"

def handle_booking(user_id, text):
    state = user_state.get(user_id)

    if not state:
        return None

    step = state["step"]

    if step == "nickname":
        state["nickname"] = text
        state["step"] = "phone"
        return "กรุณาแจ้งเบอร์โทรค่ะ"

    if step == "phone":
        state["phone"] = text
        state["step"] = "branch"
        return (
            "กรุณาเลือกสาขาที่เข้าใช้บริการค่ะ\n\n"
            "1️⃣ สาขา 1 ตลาดเชฟวันโก\n"
            "2️⃣ สาขา 2\n\n"
            "พิมพ์ 1 หรือ 2"
        )

    if step == "branch":
        if text == "1":
            state["branch"] = "สาขา 1 ตลาดเชฟวันโก"
        elif text == "2":
            state["branch"] = "สาขา 2"
        else:
            return "กรุณาเลือกสาขาเป็นเลข 1 หรือ 2 ค่ะ"

        state["step"] = "date"
        return "กรุณาแจ้งวันที่ที่ต้องการจองค่ะ\nตัวอย่าง: 27/05/2026"

    if step == "date":
        state["date"] = text
        state["step"] = "time"
        return "กรุณาแจ้งเวลาที่ต้องการจองค่ะ\nตัวอย่าง: 14:00"

    if step == "time":
        state["time"] = text
        state["step"] = "staff_choice"
        return (
            "ต้องการจองช่างประจำไหมคะ\n\n"
            "1️⃣ จองช่างประจำ\n"
            "2️⃣ ไม่จองช่างประจำ\n\n"
            "พิมพ์ 1 หรือ 2"
        )

    if step == "staff_choice":
        if text == "1":
            state["step"] = "staff_name"
            return "กรุณาระบุชื่อช่างประจำค่ะ"
        elif text == "2":
            state["staff"] = "ไม่จองช่างประจำ"

            available = is_time_available(
                state["branch"],
                state["date"],
                state["time"],
                state["staff"]
            )

            if not available:
                user_state.pop(user_id)
                return "ขออภัยค่ะ เวลานี้คิวเต็มแล้ว กรุณาพิมพ์ จองคิว เพื่อเลือกเวลาใหม่ค่ะ"

            state["step"] = "service"
            return SERVICES
        else:
            return "กรุณาพิมพ์ 1 หรือ 2 ค่ะ"

    if step == "staff_name":
        state["staff"] = text

        available = is_time_available(
            state["branch"],
            state["date"],
            state["time"],
            state["staff"]
        )

        if not available:
            user_state.pop(user_id)
            return "ขออภัยค่ะ ช่างท่านนี้มีคิวแล้วในเวลานี้ กรุณาพิมพ์ จองคิว เพื่อเลือกเวลาใหม่ค่ะ"

        state["step"] = "service"
        return SERVICES

    if step == "service":
        state["service"] = text
        state["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_booking(state)
        user_state.pop(user_id)

        return (
            "จองคิวเรียบร้อยค่ะ ✅\n\n"
            f"ชื่อเล่น: {state['nickname']}\n"
            f"เบอร์โทร: {state['phone']}\n"
            f"สาขา: {state['branch']}\n"
            f"วันที่: {state['date']}\n"
            f"เวลา: {state['time']}\n"
            f"ช่าง: {state['staff']}\n"
            f"บริการ: {state['service']}"
        )

    return "พิมพ์ว่า จองคิว เพื่อเริ่มจองคิวค่ะ"
