from datetime import datetime

from django.db.models import BooleanField, Case, When
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Правка 2 из 3: был лишний импорт модели Campaign
from referrals.models import ReferralStat
from ..serializers.gigacode import ReferralStatSerializer


class ReferralStatViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ReferralStat.objects.order_by('-created_at')
    serializer_class = ReferralStatSerializer

    def get_queryset(self):
        # Правка 1 из 3: помощник накосячил с полями в сериализаторе, поэтому считаю за него is_campaign_active тут
        return self.queryset.filter(affiliate=self.request.user).annotate(
            is_campaign_active=Case(
                When(
                    campaign__active_since__lte=datetime.today(),
                    campaign__active_till__gte=datetime.today(),
                    campaign__is_deactivated=False,
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            )
        )
