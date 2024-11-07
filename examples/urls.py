from django.urls import path
from rest_framework.authtoken import views

from .sources import (
    ENDPOINT_NAME_HUMAN,
    ENDPOINT_NAME_GITHUB_COPILOT,
    ENDPOINT_NAME_AMAZON_CODEWHISPERER,
    ENDPOINT_NAME_CHATGPT,
    ENDPOINT_NAME_GIGACODE,
    ENDPOINT_NAME_YANDEXGPT,
)
from .views.amazon_codewhisperer import ReferralStatListView as ReferralStatListViewAmazonCodeWhisperer
from .views.chatgpt import ReferralStatsListView as ReferralStatListViewChatGPT
from .views.gigacode import ReferralStatViewSet as ReferralStatListViewGigaCode
from .views.github_copilot import ReferralStatListView as ReferralStatListViewGithubCopilot
from .views.human import ReferralStatListView as ReferralStatListViewHuman
from .views.yandexgpt import ReferralStatsListAPIView as ReferralStatListViewYandexGPT

app_name = 'examples'

urlpatterns = [
    path('auth', views.obtain_auth_token),
    path('human', ReferralStatListViewHuman.as_view(), name=ENDPOINT_NAME_HUMAN),
    path('chatgpt', ReferralStatListViewChatGPT.as_view(), name=ENDPOINT_NAME_CHATGPT),
    path('github-copilot', ReferralStatListViewGithubCopilot.as_view(), name=ENDPOINT_NAME_GITHUB_COPILOT),
    path(
        'amazon-codewhisperer',
        ReferralStatListViewAmazonCodeWhisperer.as_view(),
        name=ENDPOINT_NAME_AMAZON_CODEWHISPERER,
    ),
    path('gigacode', ReferralStatListViewGigaCode.as_view({'get': 'list'}), name=ENDPOINT_NAME_GIGACODE),
    path('yandexgpt', ReferralStatListViewYandexGPT.as_view(), name=ENDPOINT_NAME_YANDEXGPT),
]
