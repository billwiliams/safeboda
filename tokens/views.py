from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tokens.serializers.serializers import PromoCodeSerializer, EventSerializer
from tokens.mixins import LoginRequiredMixin, CreateListMixin

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


class PromoCodesList(LoginRequiredMixin, CreateListMixin, APIView):
    def post(self, request, format=None):
        serializer = PromoCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
