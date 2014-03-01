from .base import FunctionalTest
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait

class RegistrationTest(FunctionalTest):

    def test_can_register(self):
        # John geht auf getraenkewart.de
        self.browser.get(self.server_url)

        # John möchte sich registrieren und klickt dazu auf Login
        self.browser.find_element_by_id("login-dropdown-button").click()
        # Er sieht einen Registrierungslink und clickt drauf
        self.browser.find_element_by_link_text("Registrieren").click()

        #Er gibt seine Daten ein
        self.browser.find_element_by_id("id_first_name").send_keys("John")
        self.browser.find_element_by_id("id_last_name").send_keys("Schmidt")
        self.browser.find_element_by_id("id_email").send_keys("jonny@provider.com")
        self.browser.find_element_by_id("id_username").send_keys("jonny")
        self.browser.find_element_by_id("id_password").send_keys("secret12")
        self.browser.find_element_by_id("id_password2").send_keys("secret12")

        # Er schickt seine Registrierung ab
        self.browser.find_element_by_id("register-button").click()

        # ... und erhält eine Bestätigung
        self.assertIn("erfolgreich angelegt", self.browser.find_element_by_class_name("alert").text)

    def test_register_error_keeps_data(self):
        first_name = "John"
        last_name = "Schmidt"
        email = "jonny@provider.com"
        username = "jonny"
        password = "secret"
        # John möchte sich registrieren
        self.browser.get(self.server_url + "/register/")

        #Er gibt seine Daten ein
        first_name_input = self.browser.find_element_by_id("id_first_name")
        first_name_input.send_keys(first_name)
        last_name_input = self.browser.find_element_by_id("id_last_name")
        last_name_input.send_keys(last_name)
        email_input = self.browser.find_element_by_id("id_email")
        email_input.send_keys(email)
        username_input = self.browser.find_element_by_id("id_username")
        username_input.send_keys(username)
        password_input = self.browser.find_element_by_id("id_password")
        password_input.send_keys(password)
        password_input2 = self.browser.find_element_by_id("id_password2")
        password_input2.send_keys(password)

        # Er schickt seine Registrierung ab
        self.browser.find_element_by_id("register-button").click()

        # ...stellt jedoch fest, dass sein Passwort zu kurz ist
        self.assertIn("muss mindestens 8 Zeichen lang sein", self.browser.find_element_by_class_name("alert").text)

        # zum Glück sind seine Daten noch da
        first_name_input = self.browser.find_element_by_id("id_first_name")
        self.assertEqual(first_name_input.get_attribute("value"), first_name)
        last_name_input = self.browser.find_element_by_id("id_last_name")
        self.assertEqual(last_name_input.get_attribute("value"), last_name)
        email_input = self.browser.find_element_by_id("id_email")
        self.assertEqual(email_input.get_attribute("value"), email)
        username_input = self.browser.find_element_by_id("id_username")
        self.assertEqual(username_input.get_attribute("value"), username)
        # mit Ausnahme der Passwörter
        password_input = self.browser.find_element_by_id("id_password")
        self.assertEqual(password_input.get_attribute("value"), "")
        password_input2 = self.browser.find_element_by_id("id_password2")
        self.assertEqual(password_input.get_attribute("value"), "")

class LoginAndLogoutTests(FunctionalTest):

    def test_registered_user_can_login_and_logout(self):
        # John ist ein registrierter Nutzer
        if not self.against_staging:
            User.objects.create_user("john", "john@provider.com", "secret12")
        else:
            self.fail("Implement against staging!")
        # John möchte sich einloggen
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("login-dropdown-button").click()
        # Er gibt seinen Benutzernamen und Passwort ein:
        self.browser.find_element_by_id("username").send_keys("john")
        self.browser.find_element_by_id("password").send_keys("secret12")
        # Und klickt auf den Login button
        self.browser.find_element_by_id("login-button").click()
        # Zufrieden stellt er fest, dass es funktioniert hat
        self.assertIn("Erfolgreich eingeloggt!", self.browser.find_element_by_class_name("alert").text)
        # Nun möchte er sich wieder ausloggen
        self.browser.find_element_by_id("logout-button").click()
        # Zufrieden stellt er fest, dass es funktioniert hat
        self.assertIn("Erfolgreich ausgeloggt!", self.browser.find_element_by_class_name("alert").text)
