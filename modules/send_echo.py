from helpers.helpers import index_in_list
from states.rex_state import RexState


def echo(data, parsed_message):
    if index_in_list(parsed_message, 2):
        RexState.chat_bot_driver.send_message(
            data["messageid"], " ".join(parsed_message[2:]))
    else:
        RexState.chat_bot_driver.send_message(data["messageid"], "Beep Boop 🤖")
