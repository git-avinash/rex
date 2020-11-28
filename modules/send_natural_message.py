from states.rex_state import RexState


def natural_message(data, parsed_message):
    response = RexState.clever_bot_driver.get_response(
        " ".join(parsed_message[1:]))
    RexState.chat_bot_driver.send_message(data["messageid"], response)
