import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as C_options
from selenium.webdriver.firefox.options import Options as F_options

from helpers.helpers import wait_for


class CleverBotWrapper(object):
    _URL = "https://www.cleverbot.com/"

    _SELECTORS = {
        "terms_confirm": "//*[@value='understood, and agreed']",
        "response": "//*[@id='line1']/span",
    }

    _last_response = None

    _end_chars = (".", "?", "!")

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

    def start(self):
        self.driver.get(self._URL)

        print(">>> Waiting for terms")
        wait_for(self.driver, self._SELECTORS["terms_confirm"])

        print(">>> Terms found now clicking")
        terms_button = self.driver.find_element_by_xpath(
            self._SELECTORS["terms_confirm"])
        terms_button.click()

        print(">>> Waiting for main page")
        wait_for(self.driver, self._SELECTORS["response"])

        print(">>> Clever Bot is Ready!")

    def _process_response(self, duration_in_sec=5):
        end_time = time.time() + duration_in_sec

        while time.time() <= end_time:
            response = self.driver.find_element_by_xpath(
                self._SELECTORS["response"]).text

            if response != self._last_response and response.endswith(self._end_chars):
                self._last_response = response
                return response

        return "Failed to get a response :("

    def get_response(self, message):
        self.driver.execute_script(f"cleverbot.sendAI(`{message}`);")
        return self._process_response()

    def quit_clever_bot(self) -> None:
        self.driver.close()
        self.driver.quit()
        self.driver.service.stop()
