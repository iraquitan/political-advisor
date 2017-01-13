from django.test import TestCase

from ..assessor.forms import AssessorForm, AssessorProfileForm


class AssessorFormTest(TestCase):
    def setUp(self):
        self.form_valid_data = {
            'first_name': 'Iraquitan', 'last_name': 'Cordeiro Filho',
            'username': "iraquitan", 'email': "leela@example.com",
            'password': "test_password",
        }

    def test_valid_data(self):
        form = AssessorForm(self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = AssessorForm({})
        self.assertFalse(form.is_valid())


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
