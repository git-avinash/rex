import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as C_options
from selenium.webdriver.firefox.options import Options as F_options
from helpers.helpers import wait_for


def filter_message_object(message_object: dict) -> dict:
    message_content = None
    message_author_id = None

    for message in message_object:
        if message['kind'] == "chat":

            for b in message["messages"]:
                message_content = b['body']

            return {
                "messageKind": message['kind'],
                "messageid": message['id'],
                "messageFrom": message['contact']['formattedName'],
                "messageContent": message_content,
            }

        if message['kind'] == "group":

            for b in message["messages"]:
                message_content = b['body']
                message_author_id = b['author']

            return {
                "messageKind": message['kind'],
                "messageid": message['id'],
                "messageFrom": message['contact']['formattedName'],
                "messageContent": message_content,
                "messageAuthorid": message_author_id,
            }


class RexWrapper(object):
    _URL = "https://web.whatsapp.com"

    _QR_FILE_NAME = "qr_code.png"

    _SELECTORS = {
        "qr_code": "//*[@data-ref]",
        "main_page": "//*[contains(text(), 'Keep your phone connected')]",
    }

    def __init__(
        self,
        headless=False,
        executable_path=None,
        options=None,
        browser="chrome",
        binary_location=None,
    ):

        if browser == "chrome":
            self._options = C_options()
            if binary_location is not None:
                self._options.binary_location = binary_location
            if headless:
                self._options.add_argument("--headless")
            if options is not None:
                for option in options:
                    self._options.add_argument(option)

            self.driver = webdriver.Chrome(
                executable_path=executable_path,
                options=self._options,
            )

        if browser == "firefox":
            self._options = F_options()
            if binary_location is not None:
                self._options.binary_location = binary_location
            if headless:
                self._options.add_argument("--headless")
            if options is not None:
                for option in options:
                    self._options.add_argument(option)

            self.driver = webdriver.Firefox(
                executable_path=executable_path,
                options=self._options,
            )

    def _inject(self) -> None:
        with open("../javascript/parasite.js", "r") as script:
            self.driver.execute_script(script.read())

    def login(self):
        # Switch to True when building
        load_qr = True

        # while load_qr is None:
        #     mode_param = str(input(
        #         "Start bot in which mode?\n1. Auth Mode (Use when Cookies are not saved)\n2. Load Cookies (Use when Cookies are saved)\n"))
        #     if mode_param == "1":
        #         load_qr = True
        #     elif mode_param == "2":
        #         load_qr = False
        #     else:
        #         print(">>> Enter a valid entry")

        self.driver.get(self._URL)

        if load_qr is True:
            wait_for(self.driver, self._SELECTORS["qr_code"])

            qr_code = self.driver.find_element_by_xpath(
                self._SELECTORS["qr_code"])
            code = qr_code.get_attribute("data-ref")
            print(
                f">>> Generate QR from https://www.the-qrcode-generator.com/ with this code:\n>>> {code}")

        wait_for(self.driver, self._SELECTORS["main_page"])

        time.sleep(1)
        self._inject()

        print(">>> Rex is Ready!")

    def get_unreads(self) -> dict:
        return self.driver.execute_script("return window.WAPI.getUnreadMessages(false,false,false);")

    def send_message(self, id: str, message: str) -> None:
        self.driver.execute_script(f"window.WAPI.sendSeen('{id}');")

        self.driver.execute_script(
            f"window.WAPI.sendMessage('{id}',`{message}`);")

    def quit_rex(self) -> None:
        self.driver.close()
        self.driver.quit()
        self.driver.service.stop()
