from django.test import TestCase

from getraenkewart.forms import (
    RegistrationForm, PASSWORDS_NOT_MATCHING_ERROR,
    PASSWORDS_TOO_SHORT_ERROR
)

class TestRegistrationForm(TestCase):
    
    def test_form_renders_correctly_first_name(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="Vorname"', form.as_p())

    def test_form_renders_correctly_last_name(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="Nachname"', form.as_p())

    def test_form_renders_correctly_username(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="Benutzername"', form.as_p())

    def test_form_renders_correctly_email(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="E-mail"', form.as_p())
        self.assertIn('type="email"', form.as_p())

    def test_form_renders_correctly_password(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="Passwort"', form.as_p())
        self.assertIn('type="password"', form.as_p())

    def test_form_renders_correctly_password2(self):
        form = RegistrationForm()
        self.assertIn('class="form-control"', form.as_p())
        self.assertIn('placeholder="Passwort bestätigen"', form.as_p())
        self.assertIn('type="password"', form.as_p())

    def test_form_checks_passwords_for_equality(self):
        form = RegistrationForm(data = { 
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"jonny",
                "email":"jon@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertTrue(form.is_valid())

    def test_form_displays_error_message_on_non_matching_passwords(self):
        form = RegistrationForm(data = { 
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"jonny",
                "email":"jon@provider.com",
                "password":"secret12",
                "password2":"secret13",
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(
                form.errors["__all__"],
                [PASSWORDS_NOT_MATCHING_ERROR]
            )

    def test_form_checks_for_minimum_password_length(self):
        form = RegistrationForm(data = { 
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"jonny",
                "email":"jon@provider.com",
                "password":"secret12",
                "password2":"secret12",
            })
        self.assertTrue(form.is_valid())

    def test_form_displays_error_on_too_short_password(self):
        form = RegistrationForm(data = { 
                "first_name":"John",
                "last_name":"Shmidt",
                "username":"jonny",
                "email":"jon@provider.com",
                "password":"secret1",
                "password2":"secret1",
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(
                form.errors["password"],
                [PASSWORDS_TOO_SHORT_ERROR]
            )
