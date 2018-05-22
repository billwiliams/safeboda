from django.shortcuts import render
from tokens.serializers.serializers import PromoCodeSerializer, EventSerializer
from tokens.mixins import LoginRequiredMixin

# Create your views here.

from tokens.models import Events, PromoCode
from rest_framework.generics import ListAPIView, CreateAPIView


class ActivePromoCodesListApiView(LoginRequiredMixin, ListAPIView):
    queryset = PromoCode.objects.order_by('-id')
    serializer_class = PromoCodeSerializer


class PromoCodesCreateApiView(LoginRequiredMixin, CreateAPIView):
    serializer_class = PromoCodeSerializer

    def perform_create(self, serializer):
        serializer.save()


class EventCreateApiView(LoginRequiredMixin, CreateAPIView):
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save()
