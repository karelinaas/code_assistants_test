from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from examples.serializers.human import ReferralStatListSerializer
from referrals.models import ReferralStat


class ReferralStatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ReferralStatListSerializer

    def get_queryset(self):
        return ReferralStat.objects.filter(affiliate=self.request.user).annotate(
            total_earned=F('campaign__reward') * F('referrals_number'),
        )
