from django.test import TestCase

from ..forms import CustomUserForm, ProfileForm, AddressForm


class CustomUserFormTest(TestCase):
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
        form = CustomUserForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = CustomUserForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_data(self):
        form = CustomUserForm(self.form_invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['Enter a valid email address.'],
            'password': ['This field is required.'],
        })


class ProfileFormTest(TestCase):
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
        form = ProfileForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = ProfileForm({})
        self.assertFalse(form.is_valid())

    def test_invalid_data(self):
        form = ProfileForm(self.form_invalid_data)
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
