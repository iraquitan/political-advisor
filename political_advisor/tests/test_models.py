from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.test import TestCase

from ..models.models import CustomUser, Address, Profile


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create_user(
            email='test_su@test.com', password='test_password', user_type='SU',
            parent=None, super_user=None
        )
        self.super_user2 = CustomUser.objects.create_user(
            email='test_su2@test.com', password='test_password',
            user_type='SU', parent=None, super_user=None
        )
        self.assessor1 = CustomUser.objects.create_user(
            email='test_parent@test.com', password='test_password',
            user_type='AU', parent=self.super_user, super_user=self.super_user
        )
        self.assessor2 = CustomUser.objects.create_user(
            email='assessor@test.com', password='test_password',
            user_type='AU', parent=self.assessor1, super_user=self.super_user
        )
        self.n1 = Group.objects.create(name='N1')
        self.n2 = Group.objects.create(name='N2')
        self.n3 = Group.objects.create(name='N3')
        self.n4 = Group.objects.create(name='N4')
        self.n5 = Group.objects.create(name='N5')

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
            CustomUser.objects.create_user(
                email='test_su@test.com', password='test_password',
                user_type='SU', parent=None, super_user=None)
            CustomUser.objects.create_user(
                email='assessor@test.com', password='test_password',
                user_type='AU', parent=self.assessor1,
                super_user=self.super_user
            )

    def test_email_user_type_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email='test_su@test.com', password='test_password',
                user_type='SU', parent=None, super_user=None)

    def test_user_group(self):
        self.assertEqual(self.super_user.groups.count(), 0)

    def test_assessor_multiple_superusers(self):
        CustomUser.objects.create_user(
            email='assessor@test.com', password='test_password',
            user_type='AU', parent=self.super_user2,
            super_user=self.super_user2)

    def test_assessor_parent_su_and_superuser_equal(self):
        for assessor in self.super_user.assessors.all():
            self.assertEqual(assessor.super_user, self.super_user)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.super_user = CustomUser.objects.create_user(
            email='test@test.com', password='test_password', user_type='SU',
            parent=None, super_user=None
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
        self.super_user = CustomUser.objects.create_user(
            email='test@test.com', password='test_password', user_type='SU',
            parent=None, super_user=None
        )
        self.address = Address.objects.create(country='Brazil',
                                              state='Pará', city='Belém',
                                              postcode='66050110',
                                              user=self.super_user)

    def test_country(self):
        self.assertEqual(self.address.country, 'Brazil')

    def test_address_user(self):
        self.assertEqual(self.address.user, self.super_user)

    def test_user_address_len(self):
        self.assertEqual(self.super_user.addresses.count(), 1)
        self.super_user.addresses.create(country='USA', state='Illinois',
                                         city='Chicago', postcode='60608')
        self.assertEqual(self.super_user.addresses.count(), 2)

    def test_user_address(self):
        self.assertEqual(self.super_user.addresses.get(postcode='66050110'),
                         self.address)
