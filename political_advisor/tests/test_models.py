from django.db import IntegrityError
from django.test import TestCase

from ..models.models import CustomUser, Address, Profile


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create(
            username='test_su', password='test_password',
            email='test_su@test.com', user_type='SU', parent=None,
            super_user=None
        )
        self.assessor1 = CustomUser.objects.create(
            username='test_parent', password='test_password',
            email='test_parent@test.com', user_type='AU',
            parent=self.super_user,
            super_user=self.super_user
        )
        self.assessor2 = CustomUser.objects.create(
            username='test_assessor', password='test_password',
            email='assessor@test.com', user_type='AU', parent=self.assessor1,
            super_user=self.super_user
        )

    def test_parent(self):
        parent = CustomUser.objects.filter(
            id=self.assessor2.parent.id
        ).get()
        self.assertEqual(self.assessor2.parent, parent)

    def test_super_user(self):
        super_user = CustomUser.objects.filter(
            id=self.assessor2.super_user.id
        ).get()
        self.assertEqual(self.assessor2.super_user, super_user)

    def test_username_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                username='test_su', password='test_password',
                email='test_su2@test.com', user_type='SU', parent=None,
                super_user=None)

    def test_email_user_type_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                username='test_su2', password='test_password',
                email='test_su@test.com', user_type='SU', parent=None,
                super_user=None)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create(
            username='test', password='test_password', email='test@test.com',
            user_type='SU', parent=None, super_user=None
        )

    def test_profile_user_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.super_user, gender='M',
                                   picture=None)

    def test_profile_created(self):
        profile = Profile.objects.filter(id=self.super_user.profile.id).get()
        self.assertEqual(self.super_user.profile, profile)
        self.assertEqual(profile.user, self.super_user)


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
