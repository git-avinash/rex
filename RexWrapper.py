import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as C_options
from selenium.webdriver.firefox.options import Options as F_options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


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

            self.driver: ChromeDriver = webdriver.Chrome(
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

            self.driver: FireFoxDriver = webdriver.Firefox(
                executable_path=executable_path,
                options=self._options,
            )

    def wait_for(self, webdriver, web_element: str, delay=60) -> bool:
        try:
            WebDriverWait(webdriver, delay).until(
                EC.presence_of_element_located((By.XPATH, web_element)))
            return True
        except TimeoutException as e:
            return False

    def _inject(self) -> None:
        with open("parasite.js", "r") as script:
            self.driver.execute_script(script.read())

        print(">>> Listning now...")

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
            self.wait_for(self.driver, self._SELECTORS["qr_code"])

            qr_code = self.driver.find_element_by_xpath(
                self._SELECTORS["qr_code"])
            code = qr_code.get_attribute("data-ref")
            print(
                f">>> Generate QR from https://www.the-qrcode-generator.com/ with this code:\n>>> {code}")

        self.wait_for(self.driver, self._SELECTORS["main_page"])

        time.sleep(1)
        self._inject()

    def get_unreads(self) -> dict:
        return self.driver.execute_script("return window.WAPI.getUnreadMessages(false,false,false);")

    def send_message(self, id: str, message: str) -> None:
        self.driver.execute_script(f"window.WAPI.sendSeen('{id}');")

        self.driver.execute_script(
            f"window.WAPI.sendMessage('{id}',`{message}`);")

    def filter_message_object(self, message_object: dict) -> dict:
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
                    message_authorid = b['author']

                return {
                    "messageKind": message['kind'],
                    "messageid": message['id'],
                    "messageFrom": message['contact']['formattedName'],
                    "messageContent": message_content,
                    "messageAuthorid": message_authorid,
                }

    def quit_rex(self) -> None:
        self.driver.close()
        self.driver.quit()
        self.driver.service.stop()
