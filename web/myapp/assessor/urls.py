from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login', views.login, name='assessor-login'),
    url(r'^assessor/register', views.register_assessor,
        name='assessor-register')
]
