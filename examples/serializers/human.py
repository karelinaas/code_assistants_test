from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatListSerializer(serializers.ModelSerializer):
    total_earned = serializers.FloatField()
    campaign = serializers.CharField(source='campaign.title')
    is_campaign_active = serializers.BooleanField()

    class Meta:
        model = ReferralStat
        fields = (
            'id',
            'campaign',
            'is_campaign_active',
            'referrals_number',
            'total_earned',
        )
