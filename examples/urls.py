from django.urls import path
from rest_framework.authtoken import views

from .sources import (
    ENDPOINT_NAME_HUMAN,
    ENDPOINT_NAME_GITHUB_COPILOT,
    ENDPOINT_NAME_AMAZON_CODEWHISPERER,
    ENDPOINT_NAME_CHATGPT,
    ENDPOINT_NAME_GIGACODE,
    ENDPOINT_NAME_YANDEX_CODE_ASSISTANT,
)
from .views.human import ReferralStatListView as ReferralStatListViewHuman
from .views.chatgpt import ReferralStatsListView as ReferralStatListViewChatGPT

app_name = 'examples'

urlpatterns = [
    path('auth', views.obtain_auth_token),
    path('human', ReferralStatListViewHuman.as_view(), name=ENDPOINT_NAME_HUMAN),
    path('chatgpt', ReferralStatListViewChatGPT.as_view(), name=ENDPOINT_NAME_CHATGPT),
]
