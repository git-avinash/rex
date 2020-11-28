from api.call_sheet import get_sheet_data
from states.rex_state import RexState


def send_meeting_links(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "Fetching Meeting Links 📫")

    sheet_data = get_sheet_data("FYBSC CS - MeetingLinks")

    ml = ["🔗", "Direct Link", "\n", "🔐", "Classroom Code", "\n"]

    for ml_obj in sheet_data:
        ml.append("\n")
        ml.append("👉")
        ml.append(ml_obj["Time"])
        ml.append("\n")
        ml.append("📕")
        ml.append(ml_obj["Subject"])
        ml.append("\n")
        ml.append("🔗")
        ml.append(ml_obj["Link"])
        ml.append("\n")
        ml.append("🔐")
        ml.append(ml_obj["Code"])
        ml.append("\n")

    RexState.chat_bot_driver.send_message(data["messageid"], " ".join(ml))
