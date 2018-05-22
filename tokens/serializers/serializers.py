from rest_framework import serializers
from tokens.models import PromoCode, Events


class PromoCodeSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Events.objects.all())

    class Meta:
        model = PromoCode
        fields = ('event', 'code', 'amount', 'active')


class PromoCodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ('active',)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('name', 'details', 'lat', 'lon', 'date')


class CodesCreateSerializer(serializers.Serializer):
    amount = serializers.IntegerField()  # amount of promo codes to give
    value_of_code = serializers.IntegerField()  # value of each promo code
    radius = serializers.IntegerField()
    event = serializers.CharField(max_length=40)
