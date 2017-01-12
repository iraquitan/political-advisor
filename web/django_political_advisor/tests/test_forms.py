from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models.models import AssessorModel, Address


class AssessorFormTest(TestCase):
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

    def test_is_valid(self):
        self.assertTrue(False, msg="Write test to check form is valid!")
