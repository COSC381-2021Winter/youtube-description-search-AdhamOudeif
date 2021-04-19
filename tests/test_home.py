from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class HomeTest(unittest.TestCase):
    def setUp(self):
        PATH="chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)

    def test_title(self):
        self.driver.get("http://localhost:5000/")
        self.assertIn("Proper Title", self.driver.title)

    def test_link(self):
    self.driver.get("http://localhost:5000/")
    link = self.driver.find_element_by_link_text("link")
    link.send_keys(Keys.RETURN)
    self.assertIn("Query", self.driver.page_source)
    self.assertIn("no search results", self.driver.page_source)



if __name__ == "__main__":
    unittest.main()
