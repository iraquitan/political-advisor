import re

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from political_advisor.models import CustomUser


class HomeViewTest(TestCase):
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


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test_user',
                                                   email='test@test.com',
                                                   password='testPassword',
                                                   first_name='Test')
        self.login_data = {'email': 'test@test.com',
                           'password': 'testPassword'}
        self.invalid_login_data = {'email': 'test2@test.com',
                                   'password': 'testPassword'}

    def test_success(self):
        response = self.client.get(reverse('login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')
        response_post = self.client.post(reverse('login'), self.login_data,
                                         follow=True)
        # Check if redirects correctly
        self.assertRedirects(response_post, reverse('home'))
        # Check messages
        messages = list(response_post.context['messages'])
        for message in messages:
            self.assertEqual(message.message, _('Welcome {user.first_name}'
                                                .format(user=self.user)))

    def test_empty_data_failure(self):
        response = self.client.get(reverse('login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')

        response_post = self.client.post(reverse('login'), {}, follow=True)
        # Check template used
        self.assertTemplateUsed(response_post, 'political_advisor/form.html')
        # Check if response is 200 OK
        self.assertEqual(response_post.status_code, 200)

    def test_unsigned_user(self):
        response = self.client.get(reverse('login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')

        response_post = self.client.post(reverse('login'),
                                         self.invalid_login_data, follow=True)
        # Check template used
        self.assertTemplateUsed(response_post, 'political_advisor/form.html')
        # Check if response is 200 OK
        self.assertEqual(response_post.status_code, 200)
        # Check messages
        messages = list(response_post.context['messages'])
        for message in messages:
            self.assertEqual(message.message, _('Login failed, user not '
                                                'found in database!'))


class SignupViewTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'main-first_name': 'Iraquitan',
            'main-last_name': 'Cordeiro Filho',
            'main-username': 'iraquitan',
            'main-password': 'testPassword',
            'main-email': 'testemail@gmail.com',
            'profile-gender': 'M', 'profile-picture': '',
        }

    def test_success(self):
        response = self.client.get(reverse('signup'))
        # Check is response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response,
                                'political_advisor/assessor_form.html')

        response_post = self.client.post(reverse('signup'), self.valid_data,
                                         follow=True)
        self.assertTemplateUsed(response_post, 'political_advisor/home.html')
        self.assertRedirects(response_post, reverse('home'))

    def test_empty_data_failure(self):
        response = self.client.get(reverse('signup'))
        # Check is response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response,
                                'political_advisor/assessor_form.html')

        response_post = self.client.post(reverse('signup'), {}, follow=True)
        self.assertTemplateUsed(response_post,
                                'political_advisor/assessor_form.html')
        self.assertEqual(response_post.status_code, 200)


class AssessorLoginViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test_user',
                                                   email='test@test.com',
                                                   password='testPassword',)
        self.assessor = CustomUser.objects.create_user(
            username='test_auser', email='test_au@test.com',
            password='testPassword', user_type='AU', parent=self.user,
            super_user=self.user,
        )
        self.login_data = {'email': 'test_au@test.com',
                           'password': 'testPassword'}
        self.invalid_login_data = {'email': 'test_au2@test.com',
                                   'password': 'testPassword'}

    def test_success(self):
        response = self.client.get(reverse('assessor-login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')
        response_post = self.client.post(reverse('assessor-login'),
                                         self.login_data, follow=True)
        # Check if redirects correctly
        self.assertRedirects(response_post, reverse('home'))

    def test_empty_data_failure(self):
        response = self.client.get(reverse('assessor-login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')

        response_post = self.client.post(reverse('assessor-login'), {},
                                         follow=True)
        # Check template used
        self.assertTemplateUsed(response_post, 'political_advisor/form.html')
        # Check if response is 200 OK
        self.assertEqual(response_post.status_code, 200)

    def test_unsigned_user(self):
        response = self.client.get(reverse('assessor-login'))
        # Check if response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check template used
        self.assertTemplateUsed(response, 'political_advisor/form.html')

        response_post = self.client.post(reverse('assessor-login'),
                                         self.invalid_login_data, follow=True)
        # Check template used
        self.assertTemplateUsed(response_post, 'political_advisor/form.html')
        # Check if response is 200 OK
        self.assertEqual(response_post.status_code, 200)
        # Check messages
        messages = list(response_post.context['messages'])
        for message in messages:
            self.assertEqual(message.message, _('Login failed, user not '
                                                'found in database!'))


class AssessorSignUpViewTest(TestCase):
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
