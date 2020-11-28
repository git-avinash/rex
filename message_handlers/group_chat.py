from modules.quit_rex import quit_rex
from modules.search_for import search_for
from modules.send_natural_message import natural_message
from modules.send_meeting_links import send_meeting_links
from modules.send_google_classroom_codes import send_google_classroom_codes
from modules.send_timetable import send_timetable
from modules.send_echo import echo
from modules.send_update_data import update_data
from modules.send_help_rex import help_rex
from modules.send_about_me import about_me
from modules.send_guide import send_guide
from states.rex_state import RexState


def group_message_handler(data):
    if data["messageContent"] is not None:

        parsed_message = data["messageContent"].split(" ")

        if RexState.is_trigger(parsed_message[0]) and len(parsed_message) >= 2:

            if data["messageid"] == "918600806187-1593763834@g.us" or data["messageid"] == "918600806187-1600503245@g.us":

                if parsed_message[1] == "help":
                    send_guide(data)

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
