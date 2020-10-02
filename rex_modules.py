from api_calls import get_sheet_data
from stringDoc import *
from rex_state import RexState


# Helper Functions
def index_in_list(list, index):
    return index <= (len(list) - 1)


# Modules
def guide(BOT, data):
    BOT.send_message(data["messageid"], guide_data_doc)


def about_me(BOT, data):
    BOT.send_message(data["messageid"], about_me_doc)


def help_rex(BOT, data):
    BOT.send_message(data["messageid"], help_rex_doc)


def update_data(BOT, data):
    BOT.send_message(data["messageid"], update_data_doc)


def no_command_exists(BOT, data, parsed_message):
    BOT.send_message(
        data["messageid"], f"You sure {' '.join(parsed_message[1:])} is the right command? 🤔 \n Use help command if you are lost 😉")


def echo(BOT, data, parsed_message):
    if index_in_list(parsed_message, 2):
        BOT.send_message(data["messageid"], " ".join(parsed_message[2:]))
    else:
        BOT.send_message(data["messageid"], "Beep Boop 🤖")


def send_timetable(BOT, data):
    BOT.send_message(data["messageid"], "Fetching TimeTable 📫")

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

    BOT.send_message(data["messageid"], " ". join(tt))


def send_google_classroom_codes(BOT, data):
    BOT.send_message(data["messageid"], "Fetching Google Classroom Codes 📫")

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

    BOT.send_message(data["messageid"], " ". join(gcc))


def send_meeting_links(BOT, data):
    BOT.send_message(data["messageid"], "Fetching Meeting Links 📫")

    sheet_data = get_sheet_data("FYBSC CS - MeetingLinks")

    ml = []

    ml.append("🔗")
    ml.append("Direct Link")
    ml.append("\n")
    ml.append("🔐")
    ml.append("Classroom Code")
    ml.append("\n")

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

    BOT.send_message(data["messageid"], " ".join(ml))


def quit_rex(BOT, data):
    if RexState.is_admin(data["messageAuthorid"]):
        BOT.send_message(
            data["messageid"], "Time to sleep 🥱")
        RexState.set_bot_loop(False)
    else:
        BOT.send_message(
            data["messageid"], "You can't access to this command!")
