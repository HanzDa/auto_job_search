# SELENIUM
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# MY CODE
from .DOM_selectors import linked_in_selectors as selectors
from scrapers.scraps_base import ScrapBase
from .filter import Filter


class JobSearchPage(ScrapBase):
    def __init__(self, driver, **kwargs):
        ScrapBase.__init__(self, driver, **kwargs)

    def _activate_filters(self):
        self.js_popup_alert_message('Activating filters')
        time.sleep(5)
        # open filters sidebar
        all_filters_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selectors.get('all_filters_button'))))
        all_filters_button.click()

        Filter.activate(self.driver, selectors.get('easy_apply_switch'))
        Filter.activate(self.driver, selectors.get('remote_jobs_input_box'))

        all_filters_button.click()  # Click again to close sidebar

    def go_to_jobs(self, position, location):
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
