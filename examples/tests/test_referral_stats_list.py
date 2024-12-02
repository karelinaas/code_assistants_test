import logging
import random
from datetime import datetime, timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import NoReverseMatch, reverse
from faker import Faker
from rest_framework.test import APIClient

from referrals.models import Affiliate, Campaign, ReferralStat
from ..sources import ENDPOINT_NAMES


class TestReferralStatsList(TestCase):
    user: Affiliate
    client: APIClient
    logger: logging.Logger

    CAMPAIGN_REWARDS = [0.25, 4, 1.10]
    REFERRALS_NUMBERS = [1222, 667, 305]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger = logging.getLogger('examples.tests')
        cls.client_class = APIClient
        faker = Faker()

        affiliates_bulk_create = [
            Affiliate(
                is_superuser=False,
                username=faker.word(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                is_staff=False,
                is_active=True,
                email=faker.email(),
            ) for _ in range(2)
        ]
        affiliates = Affiliate.objects.bulk_create(affiliates_bulk_create)
        cls.user = affiliates[0]

        campaigns_bulk_create = [
            Campaign(
                title=faker.sentence(nb_words=3),
                description=faker.sentence(nb_words=10),
                promocode=faker.word().upper(),
                reward=cls.CAMPAIGN_REWARDS[i],
                discount=random.randint(5, 10),
                active_since=datetime.today() - timedelta(days=3),
                active_till=datetime.today() + timedelta(days=3),
            ) for i in range(3)
        ]
        campaigns = Campaign.objects.bulk_create(campaigns_bulk_create)

        stats_bulk_create = [
            ReferralStat(
                campaign=campaigns[i],
                affiliate=affiliates[1] if i == 2 else cls.user,
                referrals_number=cls.REFERRALS_NUMBERS[i],
            ) for i in range(3)
        ]
        ReferralStat.objects.bulk_create(stats_bulk_create)

    def test_referral_stats_list(self):
        for endpoint_name in ENDPOINT_NAMES:
            with self.subTest(endpoint_name=endpoint_name):
                self.client.force_authenticate(user=self.user)
                try:
                    response = self.client.get(reverse(f'examples:{endpoint_name}'))
                except NoReverseMatch:
                    continue

                self.logger.info(f'1) Test {endpoint_name}`s stats list API.')

                response_data = response.json()
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(len(response_data), 2)
                self.assertTrue(response_data[1]['is_campaign_active'])
                self.assertTrue(response_data[0]['is_campaign_active'])
                self.assertEqual(response_data[1]['referrals_number'], self.REFERRALS_NUMBERS[0])
                self.assertEqual(response_data[0]['referrals_number'], self.REFERRALS_NUMBERS[1])
                self.assertEqual(response_data[1]['total_earned'], self.REFERRALS_NUMBERS[0] * self.CAMPAIGN_REWARDS[0])
                self.assertEqual(response_data[0]['total_earned'], self.REFERRALS_NUMBERS[1] * self.CAMPAIGN_REWARDS[1])
                self.assertTrue(isinstance(response_data[0]['campaign'], str), msg=endpoint_name)
                self.assertTrue(isinstance(response_data[1]['campaign'], str), msg=endpoint_name)
                self.assertEqual(
                    set(response.json()[0].keys()),
                    {'id', 'campaign', 'referrals_number', 'is_campaign_active', 'total_earned'},
                )

    def test_referral_stats_list_unauthorized(self):
        for endpoint_name in ENDPOINT_NAMES:
            with self.subTest(endpoint_name=endpoint_name):
                try:
                    response = self.client.get(reverse(f'examples:{endpoint_name}'))
                except NoReverseMatch:
                    continue

                self.logger.info(f'3) Test {endpoint_name}`s stats list API from unauthorized user.')

                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
                self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_referral_stats_list_outdated_campaigns(self):
        Campaign.objects.update(
            active_since=datetime.today() - timedelta(days=10),
            active_till=datetime.today() - timedelta(days=3),
        )

        for endpoint_name in ENDPOINT_NAMES:
            with self.subTest(endpoint_name=endpoint_name):
                self.client.force_authenticate(user=self.user)
                try:
                    response = self.client.get(reverse(f'examples:{endpoint_name}'))
                except NoReverseMatch:
                    continue

                self.logger.info(f'2) Test {endpoint_name}`s stats list API (with outdated campaigns).')

                response_data = response.json()
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(len(response_data), 2)
                self.assertFalse(response_data[1]['is_campaign_active'])
                self.assertFalse(response_data[0]['is_campaign_active'])
