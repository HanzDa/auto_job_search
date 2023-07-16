from scrapers.scraps_base import ScrapBase


class DataCollector(ScrapBase):
    def __init__(self, driver):
        ScrapBase.__init__(self, driver, driver_wait_timeout=10)

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

    def _get_recruiter_card(self):
        element = self.get_selenium_element('recruiter_card')
        return element

    def get_recruiter_name(self):
        element = self.get_selenium_element('recruiter_name_and_linked_in_url')
        return element and element.text

    def get_recruiter_linked_in_url(self):
        element = self.get_selenium_element('recruiter_name_and_linked_in_url')
        return element and element.get_attribute('href')

    def get_company_data(self):
        self.js_popup_alert_message('Getting company data...')
        # Company info
        company_name = self.get_company_name()
        company_linked_in_url = self.get_company_linked_in_url()
        company_industry = self.get_company_industry()

        return {
            'name': company_name,
            'linked_in_url': company_linked_in_url,
            'industry': company_industry,
        }

    def get_recruiter_data(self):
        self.js_popup_alert_message('Getting recruiter data...', 2)
        if not self._get_recruiter_card():
            return {}
        # recruiter info
        recruiter_name = self.get_recruiter_name()
        recruiter_linked_in_url = self.get_recruiter_linked_in_url()

        return {
            'name': recruiter_name,
            'linked_in_url': recruiter_linked_in_url,
        }

    def get_job_data(self):
        # self.js_popup_alert_message('Getting job data...')
        # Job info
        job_type = self.get_job_type()
        job_description = self.get_job_description()
        job_title = self.get_job_title()
        job_location = self.get_job_location()
        # job_posted_date = self.get_job_posted_date() Format date is required
        return {
            'type': job_type,
            'description': job_description,
            'title': job_title,
            'location': job_location,
            # 'posted_date': job_posted_date,
        }
