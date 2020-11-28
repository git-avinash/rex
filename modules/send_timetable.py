from api.call_sheet import get_sheet_data
from states.rex_state import RexState


def send_timetable(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "Fetching TimeTable 📫")

    sheet_data = get_sheet_data("FYBSC CS - TimeTable")

    tt = []

    for tt_obj in sheet_data:
        tt.append("\n")
        tt.append("▪")
        tt.append(tt_obj["Day"])
        tt.append("\n")
        tt.append("▪")
        tt.append(tt_obj["Date"])
        tt.append("\n")

        parsed_times = tt_obj["Time"].split("?")
        parsed_lectures = tt_obj["Lecture"].split("?")

        for time_lecture_obj in zip(parsed_times, parsed_lectures):
            if time_lecture_obj[0] == "":
                tt.append("📌")
                tt.append("No Lecture")
                tt.append("\n")
            if time_lecture_obj[0] == "":
                continue
            else:
                tt.append("👉")
                tt.append(time_lecture_obj[0])
                tt.append("\n")
                tt.append("📕")
                tt.append(time_lecture_obj[1])
                tt.append("\n")

    RexState.chat_bot_driver.send_message(data["messageid"], " ". join(tt))