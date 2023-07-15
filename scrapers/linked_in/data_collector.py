from time import sleep

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapers.scraps_base import ScrapBase
from .DOM_selectors import linked_in_selectors as selectors


class DataCollector(ScrapBase):
    def __init__(self, driver):
        ScrapBase.__init__(self, driver, driver_wait_timeout=10)

    @ScrapBase.sleep_time()
    def get_selenium_element(self, selector):
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

    def get_job_title(self):
        element = self.get_selenium_element('job_title')
        return element and element.text

    def get_job_type(self):
        element = self.get_selenium_element('job_type')
        return element and element.text

    def get_job_posted_date(self):
        element = self.get_selenium_element('job_posted_date')
        return element and element.text

    def get_job_description(self):
        element = self.get_selenium_element('job_description')
        return element and element.text

    def get_job_location(self):
        element = self.get_selenium_element('job_location')
        return element and element.text

    def get_company_name(self):
        element = self.get_selenium_element('company_name_and_linked_in_url')
        return element and element.text

    def get_company_linked_in_url(self):
        element = self.get_selenium_element('company_name_and_linked_in_url')
        return element.get_attribute('href')

    def get_company_industry(self):
        element = self.get_selenium_element('company_industry')
        return element and element.text

    def get_poster_name(self):
        element = self.get_selenium_element('poster_name_and_linked_in_url')
        return element and element.text

    def get_poster_linked_in_url(self):
        element = self.get_selenium_element('poster_name_and_linked_in_url')
        return element and element.get_attribute('href')

    def get_required_data(self):
        self.js_popup_alert_message('Getting job data...')
        # Job info
        job_type = self.get_job_type()
        job_description = self.get_job_description()
        job_title = self.get_job_title()
        job_location = self.get_job_location()
        job_posted_date = self.get_job_posted_date()

        # Company info
        company_name = self.get_company_name()
        company_linked_in_url = self.get_company_linked_in_url()
        company_industry = self.get_company_industry()

        # Poster info
        poster_name = self.get_poster_name()
        poster_linked_in_url = self.get_poster_linked_in_url()

        return {
            'job_type': job_type,
            'job_description': job_description or '',
            'job_title': job_title,
            'job_location': job_location,
            'job_posted_date': job_posted_date,
            'company_name': company_name,
            'company_linked_in_url': company_linked_in_url,
            'company_industry': company_industry,
            'poster_name': poster_name,
            'poster_linked_in_url': poster_linked_in_url,
        }
