from .base import LoggedInTest

class ActivationTest(LoggedInTest):

    def test_activate_registered_user(self):
        self.fail("Implement me!")
        # Chrissi will einen neu registrierten User hinzufügen

        # Er klickt dazu auf $FELD

        # Er erhält eine Übersicht von neuen Benutzern

        # Er weist den neuen User einer existierenden Person 
        # aus der Getraenkekasse hinzu

        # ... und klickt auf speichern

class SortimentTest(LoggedInTest):

    def test_enter_new_beverage(self):
        self.fail("Implement me!")
        # Chrissi will nun Weizen anbieten

        # Er klickt dazu auf $FELD

        # Er gibt Weizen in $FELD2 ein
        
        # ... und klickt auf speichern

        # Zufrieden stellt er fest, das Weizen nun in der Highscore auftaucht

class KassenTest(LoggedInTest):

    def test_updating_getraenkekasse(self):
        self.fail("Implement me!")
        # Chrissi will die aktuelle Strichliste digitalisieren

        # Dazu klickt er auf $FELD

        # Er gibt für $USER die Striche ein

        # ... und klickt auf speichern

        # Zufrieden stellt er fest, das die Striche aktualisiert wurden
