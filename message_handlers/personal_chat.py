from states.rex_state import RexState


def chat_message_handler(data):
    RexState.chat_bot_driver.send_message(
        data["messageid"], "DM listner has been implented, DM Avinash if you have any idea to use this feature 😉")
