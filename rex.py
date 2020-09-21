import os
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from RexWrapper import RexWrapper
from stringDoc import guide_data_doc, update_data_doc, help_rex_doc, about_me_doc

# Mailing Credentials
EMAIL_ADDRESS = os.environ.get("MY_EMAIL")
EMAIL_PASS = os.environ.get("MY_PASS")
MAIL_TO = "mail.avinashsah@gmail.com"


# Loading Driver and Binaries if hosted
BINARY_LOCATION = os.environ.get("GOOGLE_CHROME_BIN")
WEBDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")


# Master Debugger Switch
# Should be set to True if Hosting elsewhere
master_debug_mode = True


# Main Loop
BOT_LOOP = True


# Chrome Options
ARGS = [
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "--disable-dev-shm-usage",
    "--no-sandbox",
]
# Cookies to be saved only while debugging
# add "--user-data-dir=chrome-cookies" to ARGS to save cookies

# Bot Memory
admins = []
triggers = []


# Loading permissions
def set_permissions():
    global admins
    global triggers
    with open("bot_permissions.json", "r") as bp:
        permission = json.load(bp)
        admins = permission["admins"]
        triggers = permission["triggers"]


set_permissions()


# API Calls
def get_sheet_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             ]

    # creds.json is not Included in the repo
    # Please create your own key
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1

    timetable_data = sheet.get_all_records()

    return timetable_data


# Verification Logic

def is_admin(userid):
    for admin in admins:
        if admin == userid:
            return True
        else:
            return False


def is_trigger(trigger_message):
    for trigger in triggers:
        if trigger == trigger_message:
            return True
        else:
            return False


def index_in_list(list, index):
    return index <= (len(list) - 1)


# Handle Chat & Group

def handle_chat_call(data):
    BOT.send_message(
        data["messageid"], "DM listner has been implented, DM Avinash if you have any idea to use this feature 😉")


def handle_group_call(data):
    parsed_message = data["messageContent"].split(" ")

    if is_trigger(parsed_message[0]):

        if data["messageid"] == "918600806187-1593763834@g.us" or data["messageid"] == "918600806187-1600503245@g.us":

            if parsed_message[1] == "help":
                guide(data)

            elif parsed_message[1] == "about":
                about_me(data)

            elif parsed_message[1] == "helprex":
                help_rex(data)

            elif parsed_message[1] == "updata":
                update_data(data)

            elif parsed_message[1] == "echo":
                echo(data, parsed_message)

            elif parsed_message[1] == "tt":
                send_timetable(data)

            elif parsed_message[1] == "gcc":
                send_google_classroom_codes(data)

            elif parsed_message[1] == "ml":
                send_meeting_links(data)

            elif parsed_message[1] == "close":
                quit_bot(data)

            else:
                no_command_exists(data, parsed_message)

        else:
            BOT.send_message(
                data["messageid"], "This group is not approved, Please contact Avinash.")


# Feature Modules

def guide(data):
    BOT.send_message(data["messageid"], guide_data_doc)


def about_me(data):
    BOT.send_message(data["messageid"], about_me_doc)


def help_rex(data):
    BOT.send_message(data["messageid"], help_rex_doc)


def update_data(data):
    BOT.send_message(data["messageid"], update_data_doc)


def no_command_exists(data, parsed_message):
    BOT.send_message(
        data["messageid"], f"You sure {' '.join(parsed_message[1:])} is the right command? 🤔 \n Use help command if you are lost 😉")


def echo(data, parsed_message):
    if index_in_list(parsed_message, 2):
        BOT.send_message(data["messageid"], " ".join(parsed_message[2:]))
    else:
        BOT.send_message(data["messageid"], "Beep Boop 🤖")


def send_timetable(data):
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


def send_google_classroom_codes(data):
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


def send_meeting_links(data):
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


def quit_bot(data):
    global BOT_LOOP

    if is_admin(data["messageAuthorid"]):
        BOT.send_message(
            data["messageid"], "Time to sleep 🥱")
        BOT_LOOP = False
    else:
        BOT.send_message(
            data["messageid"], "You can't access to this command!")


# Bot Logic

BOT = RexWrapper(
    headless=master_debug_mode,
    executable_path=WEBDRIVER_PATH,
    binary_location=BINARY_LOCATION,
    options=ARGS,
)

BOT.login(
    EMAIL_ADDRESS,
    EMAIL_PASS,
    MAIL_TO,
    mail_qr_d=master_debug_mode,
)

while BOT_LOOP:
    time.sleep(1)
    messages = BOT.get_unreads()
    if not messages:
        continue
    else:
        data = BOT.filter_message_object(messages)
        print(data)

        if data["messageKind"] == "chat":
            handle_chat_call(data)

        if data["messageKind"] == "group":
            handle_group_call(data)


BOT.quit_rex()


# {
#     "messageKind": message['kind'],
#     "messageid": message['id'],
#     "messageFrom": message['contact']['formattedName'],
#     "messageContent": message_content,
#     "messageAuthorid": message_authorid, //only in group obj
# }
