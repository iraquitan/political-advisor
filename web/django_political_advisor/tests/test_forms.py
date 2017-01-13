from django.test import TestCase

from ..assessor.forms import AssessorForm, AssessorProfileForm, AddressForm


class AssessorFormTest(TestCase):
    def setUp(self):
        self.form_valid_data = {
            'first_name': 'Iraquitan', 'last_name': 'Cordeiro Filho',
            'username': "iraquitan", 'email': "leela@example.com",
            'password': "test_password",
        }
        self.form_invalid_data = {
            'first_name': 'Iraquitan', 'last_name': 'Cordeiro Filho',
            'username': "$", 'email': "e",
            'password': "",
        }

    def test_valid_data(self):
        form = AssessorForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = AssessorForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_data(self):
        form = AssessorForm(self.form_invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['Enter a valid email address.'],
            'password': ['This field is required.'],
            'username': ['Enter a valid username. This value may contain only '
                         'letters, numbers, and @/./+/-/_ characters.'],
        })


class AssessorProfileFormTest(TestCase):
    def setUp(self):
        self.form_valid_data = {
            'gender': 'M',
            'picture': None,
        }
        self.form_invalid_data = {
            'gender': 'T',
            'picture': None,
        }

    def test_valid_data(self):
        form = AssessorProfileForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = AssessorProfileForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_data(self):
        form = AssessorProfileForm(self.form_invalid_data)
        self.assertFalse(form.is_valid())


class AddressFormTest(TestCase):
    def setUp(self):
        self.form_valid_data = {
            'country': 'Brazil',
            'state': 'Pará',
            'city': 'Belém',
            'postcode': '66050110',
        }
        self.form_invalid_data = {
            'country': 'Brazil',
            'state': '',
            'city': 'Belém',
            'postcode': '66050110',
        }

    def test_valid_data(self):
        form = AddressForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = AddressForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_data(self):
        form = AddressForm(self.form_invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'state': ['This field is required.'],
        })
