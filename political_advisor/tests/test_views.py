import re

from django.test import TestCase
from django.urls import reverse


class HomeView(TestCase):
    def test_homepage(self):
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)  # Check response is 200
        # Check template used
        self.assertTemplateUsed(response1,
                                'political_advisor/home.html')
        content1 = response1.content.decode("utf-8")
        counter1 = re.search("(?<=viewed <strong>)\d+(?=</strong> times!)",
                             content1)
        counter1 = int(counter1.group()) if counter1 else 0

        response2 = self.client.get('/')
        self.assertEqual(response2.status_code, 200)  # Check response is 200
        # Check template used
        self.assertTemplateUsed(response2, 'political_advisor/home.html')
        content2 = response2.content.decode("utf-8")
        counter2 = re.search("(?<=viewed <strong>)\d+(?=</strong> times!)",
                             content2)
        counter2 = int(counter2.group()) if counter2 else 0

        # Check that page counter has increased
        self.assertGreater(counter2, counter1)


class AssessorSignUpView(TestCase):
    def setUp(self):
        self.post_valid_data = {
            'main-first_name': 'Iraquitan',
            'main-last_name': 'Cordeiro Filho',
            'main-username': 'iraquitan',
            'main-password': 'testPassword',
            'main-email': 'testemail@gmail.com',
            'profile-gender': 'M', 'profile-picture': '',
            'address-country': 'Brazil', 'address-state': 'Pará',
            'address-city': 'Belém', 'address-postcode': '66050-110'
        }

    def test_success(self):
        response = self.client.get(reverse('assessor-register'))
        # Check url path
        self.assertEqual(reverse('assessor-register'),
                         '/user/assessor/register')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that template used is assessor_form.html
        self.assertTemplateUsed(response,
                                'political_advisor/assessor_form.html')

        # Register assessor
        response = self.client.post(reverse('assessor-register'),
                                    data=self.post_valid_data, follow=True,
                                    secure=False)

        # Check if redirects to the correct page
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_failure(self):
        response = self.client.post(reverse('assessor-register'),
                                    data={}, follow=True)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that template used is assessor_form.html
        self.assertTemplateUsed(response,
                                'political_advisor/assessor_form.html')
