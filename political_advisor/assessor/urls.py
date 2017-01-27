from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login', views.login_view, name='assessor-login'),
    url(r'^assessor/register', views.register_assessor_view,
        name='assessor-register')
]
