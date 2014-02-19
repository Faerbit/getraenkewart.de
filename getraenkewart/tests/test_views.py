from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.hashers import check_password
from django.contrib.messages import constants as MSG

from getraenkewart.views import (
        login_view, logout_view, register, index,
        REGISTRATION_SUCCESS
    )
from getraenkewart.forms import RegistrationForm

class HomepageTests(TestCase):
    
    def test_home_page_uses_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed("getraenkewart/home.html")

    def test_sets_active_nav_correct(self):
        response = self.client.get("/")
        self.assertEqual(response.context["active_nav"], "start")

class RegisterTests(TestCase):

    def test_register_page_uses_register_template(self):
        response = self.client.get("/register/")
        self.assertTemplateUsed("getraenkewart/register.html")

    def test_sets_active_nav_correct(self):
        response = self.client.get("/register/")
        self.assertEqual(response.context["active_nav"], "start")

    def test_registration_page_uses_form(self):
        response = self.client.get("/register/")
        self.assertIsInstance(response.context["form"], RegistrationForm)

    def test_registration_redirects_after_success(self):
        response = self.client.post("/register/", {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertRedirects(response,"/")

    def test_registration_saves_user_to_db(self):
        response = self.client.post("/register/", {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertEqual(User.objects.all().count(), 1)
        new_user = User.objects.all()[0]
        self.assertEqual(new_user.first_name, "John")
        self.assertEqual(new_user.last_name, "Shmidt")
        self.assertEqual(new_user.username, "john")
        self.assertEqual(new_user.email, "john@provider.com")
        self.assertTrue(check_password("secret12", new_user.password))

    def test_registration_displays_success(self):
        response = self.client.post("/register/", {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertIn(REGISTRATION_SUCCESS, 
                response.cookies["messages"].value)

    def test_registration_displays_form_errors(self):
        response = self.client.post("/register/", {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret1",
                "password2":"secret1",
            })
        for message in list(response.context["messages"]):
            self.assertIn("Passwort muss mindestens 8 Zeichen lang sein.", 
                message.message)
