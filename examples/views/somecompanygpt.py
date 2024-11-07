from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from referrals.models import ReferralStat
from ..serializers.somecompanygpt import ReferralStatSerializer


class ReferralStatsListAPIView(ListAPIView):
    serializer_class = ReferralStatSerializer
    queryset = ReferralStat.objects.all().order_by('-id')

    # Правка 1 из 7: потерял permission_classes
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        # Правка 2 из 7: зачем-то искал пользователя еще раз по е-мейлу, хотя он уже есть в self.request
        # affiliate = get_object_or_404(Affiliate, email=self.request.user.email)
        # return ReferralStat.objects.filter(affiliate=affiliate).order_by('-id')
        return ReferralStat.objects.filter(affiliate=self.request.user).annotate(
            # Правка 6 из 7: неправильная логика подсчёта, добавляю сюда свой способ вычисления
            total_earned=F('campaign__reward') * F('referrals_number'),
        ).order_by('-id')
