import time
from datetime import datetime

from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

from models.company import Company
from models.job import Job
from models.recruiter import Recruiter
from scrapers.linked_in.data_collector import DataCollector
from scrapers.linked_in.login_page import LoginPage
from scrapers.linked_in.search_page import JobSearchPage
from scrapers.scraps_base import ScrapBase
from .DOM_selectors import linked_in_selectors as selectors
from .recruiter_profile import RecruiterProfile


class Scraper:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.loger = LoginPage(driver, username, password, driver_wait_timeout=10)
        self.searcher = JobSearchPage(driver, driver_wait_timeout=60)
        self.data_collector = DataCollector(driver)

    @staticmethod
    def save_scraped_data(company_data, recruiter_data, job_data):
        company = Company.get_or_create(fields=('pk',),
                                        constraints={'linked_in_url': company_data['linked_in_url']},
                                        **company_data)

        if recruiter_data:
            recruiter = Recruiter.get_or_create(fields=('pk',),
                                                constraints={'linked_in_url': recruiter_data['linked_in_url']},
                                                **recruiter_data, company_id=company.pk)
        else:
            recruiter = None

        Job.get_or_create(**job_data, company_id=company.pk, recruiter_id=recruiter and recruiter.pk)

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

    def _init_jobs_scraping(self):
        jobs_list = self.searcher.get_jobs_list()
        scraped_jobs = 0
        for job in jobs_list:
            try:
                a_tag = job.find_element(By.TAG_NAME, 'a')  # First tag should be job name clickable
                a_tag.click()
                # already_saved = self.save_job()
                # if already_saved:
                #     continue

                company_data = self.data_collector.get_company_data()
                job_data = self.data_collector.get_job_data()
                recruiter_data = self.data_collector.get_recruiter_data()

                self.save_scraped_data(company_data, recruiter_data, job_data)

                # if recruiter_data.get('linked_in_url'):
                #     recruiter_profile = RecruiterProfile(self.driver, driver_wait_timeout=10)
                #     recruiter_profile.open_new_browser_window(recruiter_data.get('linked_in_url'))
                #
                #     time.sleep(5)
                #
                #     recruiter_profile.close_window()

                scraped_jobs += 1
            except ElementClickInterceptedException:
                print('The current job card was not clickable')
            finally:
                time.sleep(1)

        print(f'--> From {len(jobs_list)} jobs available, {scraped_jobs} were scraped successfully.')

    def start(self, position, location):
        self.loger.execute()
        self.searcher.go_to_jobs(position, location)
        self._init_jobs_scraping()

        print(f'{datetime.now()} -> Scraper has finished')
