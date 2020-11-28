from states.rex_state import RexState
from static_templates.stringDoc import guide_data_doc


def send_guide(data):
    RexState.chat_bot_driver.send_message(data["messageid"], guide_data_doc)
