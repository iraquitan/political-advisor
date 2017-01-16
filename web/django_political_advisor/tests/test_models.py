from django.test import TestCase

from ..models.models import CustomUser, Address, Profile


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create(
            username='test_su', password='test_password',
            email='test_su@test.com', user_type='SU', parent=None,
            super_user=None
        )
        self.parent = CustomUser.objects.create(
            username='test_parent', password='test_password',
            email='test_parent@test.com', user_type='AU',
            parent=self.super_user,
            super_user=self.super_user
        )
        self.assessor = CustomUser.objects.create(
            username='test_assessor', password='test_password',
            email='assessor@test.com', user_type='AU', parent=self.parent,
            super_user=self.super_user
        )

    def test_parent(self):
        parent = CustomUser.objects.filter(
            id=self.assessor.parent.id
        ).get()
        self.assertEqual(self.assessor.parent, parent)

    def test_super_user(self):
        super_user = CustomUser.objects.filter(
            id=self.assessor.super_user.id
        ).get()
        self.assertEqual(self.assessor.super_user, super_user)

    def test_uniqueness(self):
        self.assertTrue(False, 'Define uniqueness test.')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create(
            username='test', password='test_password', email='test@test.com',
            user_type='SU', parent=None, super_user=None
        )
        self.profile = Profile.objects.create(user=self.super_user, gender='M',
                                              picture=None)

    def test_profile_user(self):
        self.assertEqual(self.profile.user, self.super_user)


class AddressModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create(
            username='test', password='test_password', email='test@test.com',
            user_type='SU', parent=None, super_user=None
        )
        self.address = Address.objects.create(country='Brazil',
                                              state='Pará', city='Belém',
                                              postcode='66050110',
                                              user=self.super_user)

    def test_country(self):
        self.assertEqual(self.address.country, 'Brazil')

    def test_address_user(self):
        self.assertEqual(self.address.user, self.super_user)
