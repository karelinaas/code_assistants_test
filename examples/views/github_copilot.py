from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from referrals.models import ReferralStat
from ..serializers.github_copilot import ReferralStatSerializer


class ReferralStatListView(generics.ListAPIView):
    serializer_class = ReferralStatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReferralStat.objects.filter(affiliate=self.request.user).order_by('-created_at')
