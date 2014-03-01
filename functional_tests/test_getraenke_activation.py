from django.contrib.auth.models import User
from .base import LoggedInStaffTest
from getraenke.models import Person

class ActivationTest(LoggedInStaffTest):
    
    def setUp(self):
        super().setUp()
        if not self.against_staging:
            user = User.objects.create_user("john", "", "")
            user.first_name = "John"
            user.last_name = "Shmidt"
            user.is_active = False
            user.save()
        else:
            self.fail("Implement against staging!")

    def test_activate_registered_user(self):
        # Chris will einen neu registrierten User hinzufügen
        self.browser.get(self.server_url)
        # Er klickt dazu auf "Verwalten"
        self.browser.find_element_by_id("manage-nav").click()
        # ... und dann auf "Personen"
        self.browser.find_element_by_id("people-nav").click()
        # Er erhält eine Übersicht von allen Benutzern
        self.check_for_row_in_table("people-table", "John Shmidt")
        # Er markiert den neuen Benutzer als neuer Person
        select = self.browser.find_element_by_id("john-select")
        select.select_by_visbile_text("Neuer Person")
        # ... und klickt auf speichern
        self.browser.find_element_by_id("save-button").click()
        # Zufrieden stellt er fest, dass John nun als aktiv gelistet wird
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:
            if "John Shmidt" in row.text:
                self.assertIn("aktiv", row.text)
