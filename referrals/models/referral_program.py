from django.contrib.auth.models import AbstractUser
from django.db import models

from referrals.models.base import DeactivateAbstract, TimeStampAbstract


class Campaign(TimeStampAbstract, DeactivateAbstract):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(null=True, max_length=255, verbose_name='Описание')
    promocode = models.CharField(max_length=20, verbose_name='Промокод')
    reward = models.FloatField(verbose_name='Размер вознаграждения')
    discount = models.IntegerField(null=True, blank=True, verbose_name='Размер скидки')
    active_since = models.DateField(verbose_name='Активна с')
    active_till = models.DateField(verbose_name='Активна до')

    class Meta:
        verbose_name = 'Реферальная программа'
        verbose_name_plural = 'Реферальные программы'


class Affiliate(AbstractUser, TimeStampAbstract):
    email = models.EmailField(verbose_name='E-mail', unique=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class ReferralStat(TimeStampAbstract):
    campaign = models.ForeignKey(
        Campaign,
        verbose_name='Реферальная программа',
        on_delete=models.CASCADE,
        related_name='stats',
    )
    affiliate = models.ForeignKey(
        Affiliate,
        verbose_name='Участник',
        on_delete=models.CASCADE,
        related_name='stats',
    )
    referrals_number = models.IntegerField(default=0, verbose_name='Кол-во приведённых клиентов')

    class Meta:
        verbose_name = 'Статистика по реферальной программе'
        verbose_name_plural = 'Статистика по реферальным программам'

        unique_together = ('campaign', 'affiliate',)
