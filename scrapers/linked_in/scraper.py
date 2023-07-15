import time
from datetime import datetime

from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

from scrapers.linked_in.data_collector import DataCollector
from scrapers.linked_in.login_page import LoginPage
from scrapers.linked_in.search_page import JobSearchPage
from scrapers.scraps_base import ScrapBase
from .DOM_selectors import linked_in_selectors as selectors


class Scraper:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.loger = LoginPage(driver, username, password)
        self.searcher = JobSearchPage(driver)
        self.data_collector = DataCollector(driver)

    @ScrapBase.sleep_time()
    def save_job(self):
        """ Every job will be saved to apply later, fortunately when recruiter
            had accepted the linked_in connection

            returns bool: True if job is already saved otherwise False """
        try:
            save_job_button = self.driver.find_element(By.XPATH, selectors.get('save_job_button'))
            span_tag = save_job_button.find_element(By.TAG_NAME, 'span')
            already_saved = span_tag.text.lower() == 'saved'
            if not already_saved:
                save_job_button.click()

            return already_saved
        except NoSuchElementException:
            print('Sorry, there was an error saving the job. most probably because you already applied')
            return True

    def _go_foreach_job(self):
        jobs_list = self.searcher.get_jobs_list()
        scraped_jobs = 0
        for job in jobs_list:
            try:
                a_tag = job.find_element(By.TAG_NAME, 'a')  # First tag should be job clickable name
                a_tag.click()
                already_saved = self.save_job()
                if already_saved:
                    continue

                data = self.data_collector.get_required_data()
                print(data)
                scraped_jobs += 1
            except ElementClickInterceptedException:
                print('The current job card was not clickable')
            finally:
                time.sleep(1)

        print(f'--> From {len(jobs_list)} jobs available, {scraped_jobs} were scraped successfully.')

    def start(self, position, location):
        self.loger.execute()
        self.searcher.got_to_jobs(position, location)
        self._go_foreach_job()

        print(f'{datetime.now()} -> Scraper has finished')
