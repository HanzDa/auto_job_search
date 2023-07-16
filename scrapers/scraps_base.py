from functools import wraps
from time import sleep

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome

from .linked_in.DOM_selectors import linked_in_selectors as selectors


class ScrapBase:
    def __init__(self, driver: Chrome, driver_wait_timeout=30):
        """ Constructor method.
        params:
            driver (WebDriver): web driver instance
            driver_wait_timeout (int): Time that the browser waits before crash

        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, driver_wait_timeout)

    @classmethod
    def sleep_time(cls, sleep_seconds=0):
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                sleep(sleep_seconds or 3)
                return func(*args, **kwargs)

            return inner

        return wrapper

    def js_popup_alert_message(self, message, display_seconds=5):
        js_snippet = """
            function showPopup(message, delay) {
                var popup = document.createElement('div');
                popup.textContent = message;
                popup.style.position = 'fixed';
                popup.style.top = '10px';
                popup.style.right = '10px';
                popup.style.maxWidth = '50%';
                popup.style.padding = '10px';
                popup.style.backgroundColor = '#f0f0f0';
                popup.style.color = 'black';
                popup.style.border = '1px solid #ccc';
                popup.style.borderRadius = '5px';
                popup.style.display = 'flex';
                popup.style.justifyContent = 'flex-end';
                
                document.body.appendChild(popup);
                console.log(`Delay time is: ${delay}`)
                setTimeout(() => {
                    document.body.removeChild(popup);
                }, delay);
            }
            console.log(arguments[1]);
            showPopup(arguments[0], arguments[1]);
        """

        self.driver.execute_script(js_snippet, message, display_seconds * 1000)

    def get_selenium_element(self, selector):
        sleep(2)
        tries = 2
        for _ in range(tries):
            try:
                return self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, selectors.get(selector))
                ))
            except TimeoutException:
                print(f'It seems like there was an error while trying to get {selector}')
                # trying with a different xpath selector
                selector += '_alt'
                if not selectors.get(selector):
                    break
                sleep(5)
