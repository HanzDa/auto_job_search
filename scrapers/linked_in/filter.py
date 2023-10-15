import time
from selenium.webdriver import Chrome

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class Filter:
    @staticmethod
    def activate(driver: Chrome, xpath_selector: str):
        tries = 3
        for _ in range(tries):
            time.sleep(5)
            try:
                dom_element = driver.find_element(By.XPATH, xpath_selector)
                # Simulate scroll to the element
                driver.execute_script("arguments[0].scrollIntoView();", dom_element)

                is_active = dom_element.is_selected()

                if not is_active:
                    dom_element.click()
                break

            except NoSuchElementException:
                break
