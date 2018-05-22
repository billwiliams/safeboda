from rest_framework import serializers
from tokens.models import PromoCode, Events


class PromoCodeSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Events.objects.all())

    class Meta:
        model = PromoCode
        fields = ('event', 'code', 'amount', 'active')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('name', 'details', 'lat', 'lon', 'date')
