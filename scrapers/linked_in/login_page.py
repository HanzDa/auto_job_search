# SELENIUM
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# MY CODE
from .DOM_selectors import linked_in_selectors as selectors
from scrapers.scraps_base import ScrapBase


class LoginPage(ScrapBase):
    def __init__(self, driver, user, password, **kwargs):
        self.user = user
        self.password = password
        ScrapBase.__init__(self, driver, **kwargs)

    def execute(self):
        self.js_popup_alert_message('Logging into the page...', 10)
        while True:
            try:
                user_input = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, selectors.get('user'))
                ))
                user_input.send_keys(self.user)

                password_input = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, selectors.get('password'))
                ))
                password_input.send_keys(self.password)

                login_button = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, selectors.get('login_button'))
                ))
                login_button.click()
                break
            except TimeoutException as e:
                # In case home page was loaded in other way
                print(f'There was an error while trying to login\n', e)
                time.sleep(2)
                print('Trying again...')
                self.driver.get('https://www.linkedin.com/home')
