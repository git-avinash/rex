import os
import time

from RexWrapper import RexWrapper
from CleverBotWrapper import CleverBotWrapper
from api_calls import get_sheet_data
from rex_state import RexState
from message_handler import chat_message_handler, group_message_handler


# Loading Driver and Binaries if hosted
# WEBDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
WEBDRIVER_PATH = os.environ.get("GECKODRIVER_PATH")


# Chrome Options
ARGS = [
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "--disable-dev-shm-usage",
    "--no-sandbox",
]
# Cookies to be saved only while debugging
# add "--user-data-dir=chrome-cookies" to ARGS to save cookies


# Master Debugger Switch
# Should be set to True if Hosting elsewhere
master_debug_mode = True

# Loading permissions
RexState.set_permissions()

# Instantiating Rex
print(">>> Instantiating Rex...")
rex = RexWrapper(
    headless=master_debug_mode,
    executable_path=WEBDRIVER_PATH,
    browser="firefox",
    options=ARGS,
)

rex.login()

# Instantiating Clever Bot
print(">>> Instantiating CleverBot...")
clever_bot = CleverBotWrapper(
    headless=master_debug_mode,
    executable_path=WEBDRIVER_PATH,
    browser="firefox",
    options=ARGS,
)

clever_bot.start()

# Setting state for drivers
RexState.chat_bot_driver = rex
RexState.clever_bot_driver = clever_bot

print(">>> Everything's good! Now Listning...")

while RexState.BOT_LOOP:
    time.sleep(1)
    messages = RexState.chat_bot_driver.get_unreads()
    if not messages:
        continue
    else:
        data = RexState.chat_bot_driver.filter_message_object(messages)
        print(data)

        if data["messageKind"] == "chat":
            chat_message_handler(data)

        if data["messageKind"] == "group":
            group_message_handler(data)


RexState.chat_bot_driver.quit_rex()
RexState.clever_bot_driver.quit_clever_bot()


# {
#     "messageKind": message['kind'],
#     "messageid": message['id'],
#     "messageFrom": message['contact']['formattedName'],
#     "messageContent": message_content,
#     "messageAuthorid": message_authorid, //only in group obj
# }
