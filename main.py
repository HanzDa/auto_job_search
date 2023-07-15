from dotenv import dotenv_values
from selenium import webdriver

from scrapers.linked_in.scraper import Scraper

if __name__ == '__main__':
    config = dotenv_values(".env")

    web_driver = webdriver.Chrome()
    web_driver.get(config['linked_in_url'])

    linked_in_scraper = Scraper(driver=web_driver,
                                username=config['linked_in_user'],
                                password=config['linked_in_pass'])

    position = input('What position do you want to search for?')
    location = input('What location do you want to search in?')
    linked_in_scraper.start(position, location)

    # db = Database(
    #     host=config['host'],
    #     port=config['port'],
    #     database=config['database'],
    #     user=config['user'],
    #     password=config['password'],
    # )
    #
    # db.connect()
    #
    # query = "SELECT * FROM jobs"
    # result = db.execute_query(query)
    # print(result)
    #
    # db.close_connection()
