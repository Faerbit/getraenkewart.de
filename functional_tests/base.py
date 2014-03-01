from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
import sys

class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_url = "http://" + arg.split("=")[1]
                cls.against_staging = True
                return
        LiveServerTestCase.setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            LiveServerTestCase.tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class LoggedInTest(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.against_staging:
            User.objects.create_user("chris", "chris@provider.com", "secret12")
        else:
            self.fail("Implement against staging!")

    def setUp(self):
        super().setUp()
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("login-dropdown-button").click()
        self.browser.find_element_by_id("username").send_keys("chris")
        self.browser.find_element_by_id("password").send_keys("secret12")
        self.browser.find_element_by_id("login-button").click()
