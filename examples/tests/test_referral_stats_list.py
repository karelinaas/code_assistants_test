import random
from datetime import datetime, timedelta

from django.test import TestCase
from faker import Faker

from referrals.models import Affiliate, Campaign, ReferralStat


class TestReferralStatsList(TestCase):
    user: Affiliate
    another_user: Affiliate

    CAMPAIGN_REWARDS = [0.25, 4, 1.10]
    REFERRALS_NUMBERS = [1222, 667, 305]

    def setUpClass(self) -> None:
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
        self.user = affiliates[0]
        self.another_user = affiliates[1]

        campaigns_bulk_create = [
            Campaign(
                title=faker.sentence(nb_words=3),
                description=faker.sentence(nb_words=10),
                promocode=faker.word().upper(),
                reward=self.CAMPAIGN_REWARDS[i],
                discount=random.randint(5, 10),
                active_since=datetime.today() - timedelta(days=3),
                active_till=datetime.today() + timedelta(days=3),
            ) for i in range(3)
        ]
        campaigns = Campaign.objects.bulk_create(campaigns_bulk_create)

        stats_bulk_create = [
            ReferralStat(
                campaign=campaigns[i],
                affiliate=self.another_user if i == 2 else self.user,
                referrals_number=self.REFERRALS_NUMBERS[i],
            ) for i in range(3)
        ]
        ReferralStat.objects.bulk_create(stats_bulk_create)

    def test_referral_stats_list(self):
        ...

    def test_referral_stats_list_outdated_campaigns(self):
        ...
