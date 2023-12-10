from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()  # Or any other browser
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title(self):
        self.selenium.get(f'{self.live_server_url}/your-page/')
        title = self.selenium.find_element_by_tag_name('title').get_attribute('text')
        self.assertEqual(title, 'Expected Title')
