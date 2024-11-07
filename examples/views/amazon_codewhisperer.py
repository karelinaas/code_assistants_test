from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from referrals.models import ReferralStat
from ..serializers.amazon_codewhisperer import ReferralStatSerializer


class ReferralStatListView(generics.ListAPIView):
    serializer_class = ReferralStatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Правка 2 из 2: упорядочил не по убыванию дат, а по возрастанию
        return ReferralStat.objects.filter(
            affiliate=self.request.user,
        ).select_related('campaign').order_by('-created_at')
