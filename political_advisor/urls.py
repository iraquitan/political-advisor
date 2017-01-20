from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^user/', include('political_advisor.assessor.urls')),
]
