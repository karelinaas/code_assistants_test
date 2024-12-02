from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatSerializer(serializers.ModelSerializer):
    # Правка 1 из 3: помощник использовал несуществующий у модели метод .is_active()
    # is_campaign_active = serializers.SerializerMethodField()
    is_campaign_active = serializers.BooleanField()
    total_earned = serializers.SerializerMethodField()
    # Правка 3 из 3: вместо имени программы возвращалось ID
    campaign = serializers.CharField(source='campaign.title')

    class Meta:
        model = ReferralStat
        fields = ['id', 'campaign', 'is_campaign_active', 'referrals_number', 'total_earned']

    # def get_is_campaign_active(self, obj):
    #     return obj.campaign.is_active()

    def get_total_earned(self, obj):
        return obj.campaign.reward * obj.referrals_number
