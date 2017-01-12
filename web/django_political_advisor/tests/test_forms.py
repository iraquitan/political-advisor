from django.test import TestCase

from ..assessor.forms import AssessorForm


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
