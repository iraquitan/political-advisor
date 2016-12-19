from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^assessor/register', views.register_assessor,
        name='register-assessor')
]
