# SELENIUM
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# MY CODE
from .DOM_selectors import linked_in_selectors as selectors
from scrapers.scraps_base import ScrapBase


class JobSearchPage(ScrapBase):
    def __init__(self, driver):
        ScrapBase.__init__(self, driver)

    def _activate_easy_apply(self):
        tries = 3
        for _ in range(tries):
            time.sleep(5)
            try:
                easy_apply_switch = self.driver.find_element(By.XPATH, selectors.get('easy_apply_switch'))
                # Simulate scroll to the element
                self.driver.execute_script("arguments[0].scrollIntoView();", easy_apply_switch)
                is_checked = easy_apply_switch.get_attribute('aria-checked')

                if is_checked == 'false':
                    easy_apply_switch.click()
                break

            except NoSuchElementException:
                pass

    def _activate_filters(self):
        self.js_popup_alert_message('Activating filters')
        time.sleep(5)
        all_filters_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selectors.get('all_filters_button'))))
        all_filters_button.click()
        self._activate_easy_apply()
        all_filters_button.click()  # Click again to close sidebar

    def got_to_jobs(self, position, location):
        self.js_popup_alert_message('Going to jobs', 3)
        jobs_route = f"https://www.linkedin.com/jobs/search/?f_AL=true&keywords={position}" \
                     f"&location={location}&refresh=true"
        self.driver.get(jobs_route)
        self._activate_filters()

    def get_jobs_list(self):
        self.js_popup_alert_message('Getting jobs list', 3)
        jobs_list = self.wait.until(EC.presence_of_element_located((By.XPATH, selectors.get('jobs_list'))))
        self.driver.execute_script('''
            let div = document.querySelector('#main > div > div.scaffold-layout__list > div')
            div.scrollTo({top: div.scrollHeight, behavior: 'smooth'})
        ''')
        time.sleep(3)
        return jobs_list.find_elements(By.CLASS_NAME, 'artdeco-entity-lockup')
