from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def wait_for(webdriver, web_element: str) -> None:
    delay: int = 60
    try:
        WebDriverWait(webdriver, delay).until(
            EC.presence_of_element_located((By.XPATH, web_element)))
    except TimeoutException as e:
        pass
