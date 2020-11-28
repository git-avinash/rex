from states.rex_state import RexState
from static_templates.stringDoc import about_me_doc


def about_me(data):
    RexState.chat_bot_driver.send_message(data["messageid"], about_me_doc)
