from django.utils import timezone
from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatSerializer(serializers.ModelSerializer):
    campaign = serializers.CharField(source='campaign.title', read_only=True)
    is_campaign_active = serializers.SerializerMethodField()
    total_earned = serializers.SerializerMethodField()

    class Meta:
        model = ReferralStat
        fields = ['id', 'campaign_title', 'is_campaign_active', 'referrals_number', 'total_earned']

    def get_is_campaign_active(self, obj):
        return obj.campaign.active_since <= timezone.now().date() <= obj.campaign.active_till

    def get_total_earned(self, obj):
        return obj.referrals_number * obj.campaign.reward
