from django.test import TestCase
from django.urls import reverse


class AssessorSignUpView(TestCase):
    def setUp(self):
        self.assessor = dict(first_name='Irarquitan',
                             last_name='Cordeiro Filho', username='iraquitan',
                             password='testPassword',
                             email='testemail@gmail.com')
        self.profile = dict(gender='M', picture=None)
        self.address = dict(country='Brazil', state='Pará', city='Belém',
                            postcode='66050110')
    def test_success(self):
        response = self.client.get('/user/assessor/register/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Register assessor
        data = self.assessor.copy()
        data.update(self.profile)
        data.update(self.address)
        response = self.client.post('/user/assessor/register/', data)
        self.assertEqual(response.status_code, 200)
        # Check if redirect to the correct page
        # self.assertRedirects(response, reverse('home'))
