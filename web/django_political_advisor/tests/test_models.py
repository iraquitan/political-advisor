from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models.models import AssessorModel, Address


class EntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test',
                                        password='test_password',
                                        email='test@test.com')
        user_type = ContentType.objects.get_for_model(User)
        object_id = self.user.id
        self.assessor = AssessorModel.objects.create(content_type=user_type,
                                                     object_id=object_id,
                                                     username='test_assessor',
                                                     password='test_password',
                                                     email='assessor@test.com')
        self.address = Address.objects.create(country='Brazil',
                                              state='Pará', city='Belém',
                                              postcode='66050110',
                                              user=self.assessor)

    def test_country(self):
        self.assertEqual(self.address.country, 'Brazil')

    def test_parent(self):
        parent = User.objects.filter(id=self.assessor.object_id).get()
        self.assertEqual(self.user, parent)
