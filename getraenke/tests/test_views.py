from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from getraenke.views import people
from getraenke.models import Person

class PeopleViewTests(TestCase):

    def test_correct_template_gets_used(self):
        response = self.client.get(reverse("people"))
        self.assertTemplateUsed("getraenke/people.html")

    def test_returns_new_registrations(self):
        new_user = User.objects.create_user("john")
        new_user.is_active = False
        new_user.save()
        response = self.client.get(reverse("people"))
        self.assertEqual(response.context["new_registrations"][0], 
            User.objects.all()[0])

    def test_returns_unlinked_persons(self):
        person = Person.objects.create(name="John")
        response = self.client.get(reverse("people"))
        self.assertEqual(response.context["unlinked_persons"][0], 
                Person.objects.all()[0])

    def test_returns_existing_persons(self):
        user = User.objects.create_user("john")
        person = Person.objects.create(name="John")
        person.user = user
        person.save()
        response = self.client.get(reverse("people"))
        self.assertEqual(response.context["linked_persons"][0], 
                Person.objects.all()[0])

        # test for uniqueness of person.name
