from rex_state import RexState
from rex_modules import *


def chat_message_handler(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "DM listner has been implented, DM Avinash if you have any idea to use this feature 😉")


def group_message_handler(data):
    if data["messageContent"] is not None:

        parsed_message = data["messageContent"].split(" ")

        if RexState.is_trigger(parsed_message[0]) and len(parsed_message) >= 2:

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

                elif parsed_message[1] == "search":
                    search_for(data, parsed_message)

                elif parsed_message[1] == "close":
                    quit_rex(data)

                else:
                    natural_message(data, parsed_message)

            else:
                RexState.chat_bot_driver.send_message(
                    data["messageid"], "This group is not approved, Please contact Avinash.")
