import re
from django.test import TestCase
from django.urls import reverse

from ..forms import CustomUserForm, ProfileForm, AddressForm


class HomeView(TestCase):
    def test_homepage(self):
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)  # Check response is 200
        content1 = response1.content.decode("utf-8")
        counter1 = re.search("(?<=viewed <strong>)\d+(?=</strong> times!)",
                             content1)
        counter1 = int(counter1.group()) if counter1 else 0

        response2 = self.client.get('/')
        self.assertEqual(response2.status_code, 200)  # Check response is 200
        content2 = response2.content.decode("utf-8")
        counter2 = re.search("(?<=viewed <strong>)\d+(?=</strong> times!)",
                             content2)
        counter2 = int(counter2.group()) if counter2 else 0

        # Check that page counter has increased
        self.assertGreater(counter2, counter1)


class AssessorSignUpView(TestCase):
    def setUp(self):
        self.assessor_form = CustomUserForm({'first_name': 'Iraquitan',
                                             'last_name': 'Cordeiro Filho',
                                             'username': 'iraquitan',
                                             'password': 'testPassword',
                                             'email': 'testemail@gmail.com'},
                                            prefix='main')
        self.profile_form = ProfileForm({'gender': 'M',
                                         'picture': None},
                                        prefix='profile')
        self.address_form = AddressForm({'country': 'Brazil', 'state': 'Pará',
                                         'city': 'Belém',
                                         'postcode': '66050110'},
                                        prefix='address')
        self.post_valid_data = {
            'id_main-first_name': 'Iraquitan',
            'id_main-last_name': 'Cordeiro Filho',
            'id_main-username': 'iraquitan',
            'id_main-password': 'testPassword',
            'id_main-email': 'testemail@gmail.com',
            'id_profile-gender': 'M', 'id_profile-picture': None,
            'id_address-country': 'Brazil', 'id_address-state': 'Pará',
            'id_address-city': 'Belém', 'id_address-postcode': '66050110'
        }

    def test_success(self):
        response = self.client.get(reverse('assessor-register'))
        # Check url path
        self.assertEqual(reverse('assessor-register'),
                         '/user/assessor/register')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Register assessor
        # self.assertTrue(all([self.assessor_form.is_valid(),
        #                      self.profile_form.is_valid(),
        #                      self.address_form.is_valid()]))
        # new_assessor = self.assessor_form.save()
        # profile = self.profile_form.save(commit=False)
        # address = self.address_form.save(commit=False)
        # new_assessor.profile = profile
        # new_assessor.addresses.add(address)
        # self.assessor_form.save_m2m()
        #
        # self.assertEqual(new_assessor.profile.gender, "M")
        # address = new_assessor.addresses[0]
        # self.assertEqual(address.country, "Brazil")
        # self.assertEqual(address.state, "Pará")
        # self.assertEqual(address.city, "Belém")
        # self.assertEqual(address.postcode, "66050110")

        # data = self.assessor.copy()
        # data.update(self.profile)
        # data.update(self.address)
        # print(data)
        response = self.client.post(reverse('assessor-register'),
                                    data=self.post_valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if redirect to the correct page
        # self.assertRedirects(response, reverse('home'))
        # self.assertRedirects(response, reverse('home'), 302, 200)
        # # self.assertRedirects(response, '/')
