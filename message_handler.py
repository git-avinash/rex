from rex_state import RexState
from rex_modules import *


def chat_message_handler(BOT, data):
    BOT.send_message(
        data["messageid"], "DM listner has been implented, DM Avinash if you have any idea to use this feature 😉")


def group_message_handler(BOT, data):
    if data["messageContent"] is not None:

        parsed_message = data["messageContent"].split(" ")

        if RexState.is_trigger(parsed_message[0]):

            if data["messageid"] == "918600806187-1593763834@g.us" or data["messageid"] == "918600806187-1600503245@g.us":

                if parsed_message[1] == "help":
                    guide(BOT, data)

                elif parsed_message[1] == "about":
                    about_me(BOT, data)

                elif parsed_message[1] == "helprex":
                    help_rex(BOT, data)

                elif parsed_message[1] == "updata":
                    update_data(BOT, data)

                elif parsed_message[1] == "echo":
                    echo(BOT, data, parsed_message)

                elif parsed_message[1] == "tt":
                    send_timetable(BOT, data)

                elif parsed_message[1] == "gcc":
                    send_google_classroom_codes(BOT, data)

                elif parsed_message[1] == "ml":
                    send_meeting_links(BOT, data)

                elif parsed_message[1] == "close":
                    quit_rex(BOT, data)

                else:
                    no_command_exists(BOT, data, parsed_message)

            else:
                BOT.send_message(
                    data["messageid"], "This group is not approved, Please contact Avinash.")
