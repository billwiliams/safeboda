from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tokens.serializers.serializers import PromoCodeSerializer, EventSerializer, CodesCreateSerializer
from tokens.mixins import LoginRequiredMixin, CreateListMixin
from rest_framework import authentication, permissions
from tokens.promo_codes import GeneratePromoCodes

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


class PromoCodesList(LoginRequiredMixin, APIView):
    """
        View to list all users in the system.

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    # def get(self, request, format=None):
    #     """
    #     Return a list of all users.
    #     """
    #     usernames = [user.username for user in User.objects.all()]
    #     return Response(usernames)

    def post(self, request, format=None):
        serializer1 = CodesCreateSerializer(data=request.data)

        if serializer1.is_valid():
            number_of_promo_codes = request.data["amount"] / request.data["worth"]
            code_generator = GeneratePromoCodes()
            promo_codes = []
            for i in range(int(number_of_promo_codes)):
                promo_codes.append(code_generator.promo_code())
            # serializer.save()
            return Response(promo_codes, status=status.HTTP_201_CREATED)
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
