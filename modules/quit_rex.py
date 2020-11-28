from states.rex_state import RexState


def quit_rex(data):
    if RexState.is_admin(data["messageAuthorid"]):
        RexState.chat_bot_driver.send_message(
            data["messageid"], "Time to sleep 🥱")
        RexState.BOT_LOOP = False
    else:
        RexState.chat_bot_driver.send_message(
            data["messageid"], "You can't access this command!")
