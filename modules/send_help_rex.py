from states.rex_state import RexState
from static_templates.stringDoc import help_rex_doc


def help_rex(data):
    RexState.chat_bot_driver.send_message(data["messageid"], help_rex_doc)
