from time import timezone

from django.utils import timezone
from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatSerializer(serializers.ModelSerializer):
    is_campaign_active = serializers.SerializerMethodField()
    total_earned = serializers.SerializerMethodField()

    class Meta:
        model = ReferralStat
        fields = ['id', 'campaign', 'is_campaign_active', 'referrals_number', 'total_earned']

    def get_is_campaign_active(self, obj):
        today = timezone.now().date()
        return obj.campaign.active_since <= today <= obj.campaign.active_till

    def get_total_earned(self, obj):
        return obj.referrals_number * obj.campaign.reward
