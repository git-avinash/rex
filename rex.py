import os
import time

from web_wrappers.RexWrapper import RexWrapper, filter_message_object
from web_wrappers.CleverBotWrapper import CleverBotWrapper
from states.rex_state import RexState
from message_handlers.group_chat import group_message_handler
from message_handlers.personal_chat import chat_message_handler

# Loading Driver and Binaries if hosted
# WEB_DRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
WEB_DRIVER_PATH = os.environ.get("GECKODRIVER_PATH")

# Chrome Options
ARGS = [
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 "
    "Safari/537.36",
    "--disable-dev-shm-usage",
    "--no-sandbox",
]
# Cookies to be saved only while debugging
# add "--user-data-dir=chrome-cookies" to ARGS to save cookies


# Master Debugger Switch
# Should be set to True if Hosting elsewhere
master_debug_mode = True

if __name__ == "__main__":
    # Loading permissions
    RexState.set_permissions()

    # Instantiating Rex
    print(">>> Instantiating Rex...")
    rex = RexWrapper(
        headless=master_debug_mode,
        executable_path=WEB_DRIVER_PATH,
        browser="firefox",
        options=ARGS,
    )

    rex.login()

    # Instantiating Clever Bot
    print(">>> Instantiating CleverBot...")
    clever_bot = CleverBotWrapper(
        headless=master_debug_mode,
        executable_path=WEB_DRIVER_PATH,
        browser="firefox",
        options=ARGS,
    )

    clever_bot.start()

    # Setting state for drivers
    RexState.chat_bot_driver = rex
    RexState.clever_bot_driver = clever_bot

    print(">>> Everything's good! Now Listning...")

    # Main Bot Loop
    while RexState.BOT_LOOP:
        time.sleep(1)
        messages = RexState.chat_bot_driver.get_unreads()
        if not messages:
            continue
        else:
            data = filter_message_object(messages)
            print(data)

            if data["messageKind"] == "chat":
                chat_message_handler(data)

            if data["messageKind"] == "group":
                group_message_handler(data)

    # Exists on loop break
    RexState.chat_bot_driver.quit_rex()
    RexState.clever_bot_driver.quit_clever_bot()

# {
#     "messageKind": message['kind'],
#     "messageid": message['id'],
#     "messageFrom": message['contact']['formattedName'],
#     "messageContent": message_content,
#     "messageAuthorid": message_authorid, //only in group obj
# }
