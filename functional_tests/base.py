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

    def check_for_row_in_table(self, table_id, row_text):
            table = self.browser.find_element_by_id(table_id)
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(row_text, [row.text for row in rows])

class LoggedInStaffTest(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.against_staging:
            user = User.objects.create_user("chris", "chris@provider.com", "secret12")
            user.is_staff = True
            user.save()
        else:
            self.fail("Implement against staging!")

    def setUp(self):
        super().setUp()
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("login-dropdown-button").click()
        self.browser.find_element_by_id("username").send_keys("chris")
        self.browser.find_element_by_id("password").send_keys("secret12")
        self.browser.find_element_by_id("login-button").click()
