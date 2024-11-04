import random

from django.core import management
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from referrals.models import Affiliate, Campaign, ReferralStat, ReferralStatSimplified


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    STATS_MAP = {
        0: [0, 1],
        1: [3],
        2: [1, 2, 3],
    }

    __faker: Faker
    __campaign_pks: list[int] = []
    __campaign_promocodes: list[str] = []
    __affiliate_pks: list[int] = []
    __affiliate_usernames: list[str] = []

    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.__faker = Faker()


    def handle(self, *args, **options):
        with transaction.atomic():
            self.__seed_campaigns()
            self.__seed_affiliates()
            self.__seed_stats()
            self.__seed_stats_simple()

    def __seed_campaigns(self):
        if Campaign.objects.count() < 3:
            management.call_command('loaddata', 'campaign', verbosity=0)
        self.__campaign_pks = Campaign.objects.values_list('pk', flat=True)
        self.__campaign_promocodes = Campaign.objects.values_list('promocode', flat=True)

    def __seed_affiliates(self):
        affiliates_bulk_create = []

        for _ in range(0, 4):
            username = self.__faker.word()
            self.__affiliate_usernames.append(username)

            affiliate = Affiliate(
                is_superuser=False,
                username=username,
                first_name=self.__faker.first_name(),
                last_name=self.__faker.last_name(),
                is_staff=False,
                is_active=True,
                email=self.__faker.email(),
            )
            affiliate.set_password(self.__faker.password())

            affiliates_bulk_create.append(affiliate)

        affiliates = Affiliate.objects.bulk_create(affiliates_bulk_create)
        self.__affiliate_pks = [affiliate.pk for affiliate in affiliates]

    def __seed_stats(self):
        stats_bulk_create = []

        for campaign_num, affiliate_nums in self.STATS_MAP.items():
            for affiliate_num in affiliate_nums:
                stats_bulk_create.append(
                    ReferralStat(
                        campaign_id=self.__campaign_pks[campaign_num],
                        affiliate_id=self.__affiliate_pks[affiliate_num],
                        referrals_number=random.randint(100, 1000),
                    )
                )

        ReferralStat.objects.bulk_create(stats_bulk_create)

    def __seed_stats_simple(self):
        stats_bulk_create = []

        for campaign_num, affiliate_nums in self.STATS_MAP.items():
            for affiliate_num in affiliate_nums:
                stats_bulk_create.append(
                    ReferralStatSimplified(
                        promocode=self.__campaign_promocodes[campaign_num],
                        username=self.__affiliate_usernames[affiliate_num],
                        referrals_number=random.randint(100, 1000),
                    )
                )

        ReferralStatSimplified.objects.bulk_create(stats_bulk_create)
