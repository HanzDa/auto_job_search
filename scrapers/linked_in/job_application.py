from scrapers.scraps_base import ScrapBase


class Applicant(ScrapBase):
    def __init__(self, driver):
        ScrapBase.__init__(self, driver, 10)

    def apply_to_saved_jobs(self):
        # Is this opsolete or shall I implement it?
        # self.driver.get('https://www.linkedin.com/my-items/saved-jobs/?cardType=SAVED')
        pass

    def easy_apply(self):
        """ Apply to the linkedin job that has easy to apply option """
