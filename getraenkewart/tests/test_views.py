from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.hashers import check_password
from django.contrib.messages import constants as MSG
from django.core.urlresolvers import reverse

from getraenkewart.views import (
        REGISTRATION_SUCCESS, LOGIN_SUCCESFUL, LOGOUT_SUCCESFUL,
        WRONG_PASSWORD_ERROR, NOT_ACTIVE_ERROR
    )
from getraenkewart.forms import RegistrationForm

class HomepageTests(TestCase):
    
    def test_home_page_uses_home_page_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed("getraenkewart/home.html")

class LoginTests(TestCase):

    def test_user_can_login(self):
        User.objects.create_user("john", "", "secret12")
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertIn(LOGIN_SUCCESFUL, 
            response.cookies["messages"].value)

    def test_redirects_after_login(self):
        User.objects.create_user("john", "", "secret12")
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertRedirects(response, reverse("index"))

    def test_gives_appropriate_error_if_user_is_not_active(self):
        User.objects.create_user("john", "", "secret12")
        user = User.objects.all()[0]
        user.is_active = False
        user.save()
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertIn(NOT_ACTIVE_ERROR, 
            response.cookies["messages"].value)

    def test_redirects_after_not_active_error(self):
        User.objects.create_user("john", "", "secret12")
        user = User.objects.all()[0]
        user.is_active = False
        user.save()
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertRedirects(response, reverse("index"))

    def test_gives_appropriate_error_if_the_password_is_wrong(self):
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertIn(WRONG_PASSWORD_ERROR, 
            response.cookies["messages"].value)

    def test_redirects_after_wrong_password_error(self):
        response = self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        self.assertRedirects(response, reverse("index"))

class LogoutTests(TestCase):
    
    def test_user_can_logout(self):
        User.objects.create_user("john", "", "secret12")
        # log user in to let him logout
        self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        response = self.client.post(reverse("logout"))
        self.assertIn(LOGOUT_SUCCESFUL, 
            response.cookies["messages"].value)

    def test_logout_redirects_after_logout(self):
        User.objects.create_user("john", "", "secret12")
        # log user in to let him logout
        self.client.post(reverse("login"), {
            "username":"john",
            "password":"secret12"
            })
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index"))

class RegisterTests(TestCase):

    def test_register_page_uses_register_template(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed("getraenkewart/register.html")

    def test_registration_page_uses_form(self):
        response = self.client.get(reverse("register"))
        self.assertIsInstance(response.context["form"], RegistrationForm)

    def test_registration_redirects_after_success(self):
        response = self.client.post(reverse("register"), {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertRedirects(response,reverse("index"))

    def test_registration_saves_user_to_db(self):
        response = self.client.post(reverse("register"), {
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
        self.assertFalse(new_user.is_active)
        self.assertTrue(check_password("secret12", new_user.password))

    def test_registration_displays_success(self):
        response = self.client.post(reverse("register"), {
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
        response = self.client.post(reverse("register"), {
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"john",
                "email":"john@provider.com",
                "password":"secret1",
                "password2":"secret1",
            })
        for msgObject in list(response.context["messages"]):
            self.assertIn("Passwort muss mindestens 8 Zeichen lang sein.", 
                msgObject.message)
