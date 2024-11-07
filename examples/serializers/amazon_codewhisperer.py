from rest_framework import serializers
from django.utils import timezone

# Правка 1 из 2: был лишний импорт модели Campaign
from referrals.models import ReferralStat


class ReferralStatSerializer(serializers.ModelSerializer):
    campaign = serializers.CharField(source='campaign.title')
    is_campaign_active = serializers.SerializerMethodField()
    total_earned = serializers.SerializerMethodField()

    class Meta:
        model = ReferralStat
        fields = ['id', 'campaign', 'is_campaign_active', 'referrals_number', 'total_earned']

    def get_is_campaign_active(self, obj):
        now = timezone.now().date()
        return obj.campaign.active_since <= now <= obj.campaign.active_till and not obj.campaign.is_deactivated

    def get_total_earned(self, obj):
        return obj.referrals_number * obj.campaign.reward
