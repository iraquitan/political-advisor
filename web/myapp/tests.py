from django.test import TestCase


# Create your tests here.
class BaseTest(TestCase):
    def base_test(self):
        self.assertEqual(1, 1)
