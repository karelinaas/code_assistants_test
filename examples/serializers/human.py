from rest_framework import serializers

from referrals.models import ReferralStat


class ReferralStatListSerializer(serializers.ModelSerializer):
    total_earned = serializers.FloatField()
    campaign = serializers.CharField(source='campaign.title')

    class Meta:
        model = ReferralStat
        fields = (
            'id',
            'campaign',
            'referrals_number',
            'total_earned',
        )
