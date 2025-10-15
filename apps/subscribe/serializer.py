from rest_framework import serializers
from django.utils import timezone

from .models import SubscriptionPlan, Subscription, \
    PinnedPost, SubscriptionHistory


class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'price', 'duration_days', 'features',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):

        data = super().to_representation(instance)

        # впевнеться шо features обьєкт
        if not data.get('features'):
            data['features'] = {}

        return data
