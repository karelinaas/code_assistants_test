import datetime

from django.db.models import Sum
from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatSerializer(serializers.ModelSerializer):
    is_campaign_active = serializers.SerializerMethodField()
    # Правка 3 из 7: намудрил с определением поля
    # total_earned = serializers.IntegerField(source='get_total_earned', read_only=True)
    total_earned = serializers.FloatField()
    # Правка 7 из 7: вместо имени программы возвращалось ID
    campaign = serializers.CharField(source='campaign.title')

    class Meta:
        model = ReferralStat
        fields = [
            'id',
            'campaign',
            'affiliate',
            'referrals_number',
            'is_campaign_active',
            'total_earned',
        ]

    def get_is_campaign_active(self, instance):
        current_date = datetime.date.today()
        return instance.campaign.active_since <= current_date <= instance.campaign.active_till

    # Правка 6 из 7: неправильная логика подсчёта
    def get_total_earned(self, instance):
        # Правка 4 из 7: ошибка "Complex aggregates require an alias"
        earnings = instance.affiliate.stats.aggregate(
            referrals_number__sum=Sum('referrals_number') * instance.campaign.reward
        )
        # Правка 5 из 7: ошибка из-за earnings[0]
        return earnings['referrals_number__sum'] * instance.campaign.reward if earnings else 0
