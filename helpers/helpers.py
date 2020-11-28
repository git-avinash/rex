from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def index_in_list(list, index):
    return index <= (len(list) - 1)


def wait_for(web_driver, web_element: str, delay=60) -> bool:
    try:
        WebDriverWait(web_driver, delay).until(
            ec.presence_of_element_located((By.XPATH, web_element)))
        return True
    except TimeoutException as e:
        return False
