from .base import FunctionalTest

class RegistrationTest(FunctionalTest):

    def test_can_register(self):
        # Jonas geht auf getraenkewart.de
        self.browser.get(self.server_url)

        # Jonas möchte sich registrieren und klickt dazu auf Login
        self.browser.find_element_by_id("login-dropdown-button").click()
        # Er sieht einen Registrierungslink und clickt drauf
        self.browser.find_element_by_link_text("Registrieren").click()

        #Er gibt seine Daten ein
        self.browser.find_element_by_id("first_name").send_keys("Jonas")
        self.browser.find_element_by_id("last_name").send_keys("Schmidt")
        self.browser.find_element_by_id("e-mail").send_keys("jonny@provider.com")
        self.browser.find_element_by_id("username").send_keys("jonny")
        self.browser.find_element_by_id("password").send_keys("secret12")

        # Er schickt seine Registrierung ab

        self.browser.find_element_by_tag_name("button").click()

        # ... und erhält eine Bestätigung

        self.assertIn("erfolgreich angelegt", self.browser.find_element_by_class("alert").text)
