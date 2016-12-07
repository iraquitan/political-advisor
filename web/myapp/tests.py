from django.test import TestCase


# Create your tests here.
class BaseTests(TestCase):
    def test_base(self):
        self.assertEqual(True, False)
