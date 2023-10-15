from scrapers.scraps_base import ScrapBase


class RecruiterProfile(ScrapBase):
    def __init__(self, driver, **kwargs):
        ScrapBase.__init__(self, driver, **kwargs)

    def send_connection_request(self, url):
        pass

    def send_message(self, message):
        pass
