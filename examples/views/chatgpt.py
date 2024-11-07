from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from referrals.models import ReferralStat
from ..serializers.chatgpt import ReferralStatSerializer


class ReferralStatsListView(generics.ListAPIView):
    serializer_class = ReferralStatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ReferralStat.objects.filter(affiliate=user).order_by('-created_at')
