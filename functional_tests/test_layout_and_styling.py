from .base import FunctionalTest

class LayoutAndStyling(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)

        login_box = self.browser.find_element_by_id("username")

        self.assertFalse(login_box.is_displayed(), "CSS isn't loaded")
