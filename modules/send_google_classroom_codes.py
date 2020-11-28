from api.call_sheet import get_sheet_data
from states.rex_state import RexState


def send_google_classroom_codes(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "Fetching Google Classroom Codes 📫")

    sheet_data = get_sheet_data("FYBSC CS - GoogleClassroomCodes")

    gcc = []

    gcc.append("🔗")
    gcc.append("Direct Link")
    gcc.append("\n")
    gcc.append("🔐")
    gcc.append("Classroom Code")
    gcc.append("\n")

    for gcc_obj in sheet_data:

        gcc.append("\n")

        for topic in gcc_obj["Topic"].split("?"):
            gcc.append("▪")
            gcc.append(topic)

        gcc.append("\n")
        gcc.append("🔗")
        gcc.append(gcc_obj["Link"])
        gcc.append("\n")
        gcc.append("🔐")
        gcc.append(gcc_obj["Code"])
        gcc.append("\n")

    RexState.chat_bot_driver.send_message(data["messageid"], " ".join(gcc))
