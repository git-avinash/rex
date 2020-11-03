import wikipedia

from api_calls import get_sheet_data
from stringDoc import *
from rex_state import RexState


# Helper Functions
def index_in_list(list, index):
    return index <= (len(list) - 1)


# Modules
def guide(data):
    RexState.chat_bot_driver.send_message(data["messageid"], guide_data_doc)


def about_me(data):
    RexState.chat_bot_driver.send_message(data["messageid"], about_me_doc)


def help_rex(data):
    RexState.chat_bot_driver.send_message(data["messageid"], help_rex_doc)


def update_data(data):
    RexState.chat_bot_driver.send_message(data["messageid"], update_data_doc)


def echo(data, parsed_message):
    if index_in_list(parsed_message, 2):
        RexState.chat_bot_driver.send_message(
            data["messageid"], " ".join(parsed_message[2:]))
    else:
        RexState.chat_bot_driver.send_message(data["messageid"], "Beep Boop 🤖")


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

    RexState.chat_bot_driver.send_message(data["messageid"], " ". join(gcc))


def send_meeting_links(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "Fetching Meeting Links 📫")

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

    RexState.chat_bot_driver.send_message(data["messageid"], " ".join(ml))


def natural_message(data, parsed_message):
    response = RexState.clever_bot_driver.get_response(
        " ".join(parsed_message[1:]))
    RexState.chat_bot_driver.send_message(data["messageid"], response)


def search_for(data, parsed_message):
    def isMode(mode):
        modes = ("l", "p", "all")

        for mode_str in modes:
            if mode_str == mode:
                return True

        return False

    def wiki(query, mode="l"):
        try:
            solved_query = []

            response = wikipedia.summary(query)
            parsed_paragraphs = response.split("\n")
            number_of_paragraphs = len(parsed_paragraphs)
            first_paragraph_lines = parsed_paragraphs[0].split(".")
            number_of_lines_in_first_paragraph = len(first_paragraph_lines)

            if mode == "all":
                return response

            if mode == "p":
                solved_query.append(parsed_paragraphs[0])

                if number_of_paragraphs > 1:
                    solved_query.append("\n\n")
                    solved_query.append(
                        f"\n📌 Showing *1/{number_of_paragraphs} paragraph* to read.")
                    solved_query.append(
                        f"\n📌 Add **all** tag to get the whole article.")
                    solved_query.append(
                        f"\n📌 *Example: @Rex search {query} all*")

                return " ".join(solved_query)

            if mode == "l":
                solved_query.append(first_paragraph_lines[0])

                if number_of_lines_in_first_paragraph > 1:
                    solved_query.append("\n")
                    solved_query.append(
                        f"\n📌 This query has total *{number_of_lines_in_first_paragraph-1} more lines* ")

                if number_of_paragraphs > 1:
                    solved_query.append(
                        f"and *{number_of_paragraphs} paragraphs* to read.")

                solved_query.append(
                    f"\n📌 Add **p** tag to read first paragraph or **all** tag to get the whole article.")
                solved_query.append(f"\n📌 *Example: @Rex search {query} p/all*")

                return " ".join(solved_query)

        except:
            return f"Couldn't find results for *'{query}'* 😩"

    if len(parsed_message) > 2:

        if not isMode(parsed_message[-1]):
            parsed_message.append("l")

        result = wiki(" ".join(parsed_message[2:-1]), mode=parsed_message[-1])
        RexState.chat_bot_driver.send_message(data["messageid"], result)

    else:
        RexState.chat_bot_driver.send_message(
            data["messageid"], "Please pass a query to search!")


def quit_rex(data):
    if RexState.is_admin(data["messageAuthorid"]):
        RexState.chat_bot_driver.send_message(
            data["messageid"], "Time to sleep 🥱")
        RexState.BOT_LOOP = False
    else:
        RexState.chat_bot_driver.send_message(
            data["messageid"], "You can't access this command!")
