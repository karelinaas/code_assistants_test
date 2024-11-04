from django.urls import path
from rest_framework.authtoken import views

from examples.views.human import ReferralStatListView

app_name = 'examples'

urlpatterns = [
    path('auth', views.obtain_auth_token),
    path('human', ReferralStatListView.as_view(), name='human')
]
