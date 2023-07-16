from scrapers.scraps_base import ScrapBase


class JobApplication(ScrapBase):
    def __init__(self, driver):
        ScrapBase.__init__(self, driver, 10)

    def start_to_apply(self):
        self.driver.get('https://www.linkedin.com/my-items/saved-jobs/?cardType=SAVED')
