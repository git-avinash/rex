from states.rex_state import RexState
from static_templates.stringDoc import update_data_doc


def update_data(data):
    RexState.chat_bot_driver.send_message(data["messageid"], update_data_doc)
