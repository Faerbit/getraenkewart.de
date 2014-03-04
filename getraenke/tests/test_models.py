from django.test import TestCase
from django.contrib.auth.models import User

from getraenke.models import Person, Jahr

class PersonTest(TestCase):

    def test_person_representation(self):
        p = Person(name="John")
        self.assertEqual(str(p), p.name)

    def test_person_isnt_linked_to_any_user_per_default(self):
        p = Person(name="John")
        with self.assertRaises(User.DoesNotExist):
            p.user

    def test_person_can_be_associated_with_jahr_object(self):
        jahr = Jahr(jahr=503)
        jahr.save()
        person = Person(name="John")
        person.save()
        person.jahre.add(jahr)
        self.assertEqual(jahr, person.jahre.filter(jahr__exact=503)[0])
