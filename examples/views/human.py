from datetime import datetime

from django.db.models import BooleanField, Case, F, When
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from referrals.models import ReferralStat
from ..serializers.human import ReferralStatListSerializer


class ReferralStatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferralStatListSerializer

    def get_queryset(self):
        return ReferralStat.objects.select_related('campaign').filter(
            affiliate=self.request.user,
        ).annotate(
            total_earned=F('campaign__reward') * F('referrals_number'),
            is_campaign_active=Case(
                When(
                    campaign__active_since__lte=datetime.today(),
                    campaign__active_till__gte=datetime.today(),
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            )
        ).order_by('-pk')
