from django.db import models


class ReferralStatSimplified(models.Model):
    promocode = models.CharField(max_length=10, verbose_name='Промокод')
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    referrals_number = models.IntegerField(default=0, verbose_name='Кол-во приведённых клиентов')

    class Meta:
        verbose_name = 'Упрощённая статистика'
        verbose_name_plural = 'Упрощённая статистика'

        unique_together = ('promocode', 'username',)
