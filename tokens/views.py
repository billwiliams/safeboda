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
        serializer = CodesCreateSerializer(data=request.data)

        if serializer.is_valid():
            number_of_promo_codes = request.data["amount"] / request.data["value_of_code"]
            event = Events.objects.filter(name__exact=request.data["event"])
            code_generator = GeneratePromoCodes()

            for i in range(int(number_of_promo_codes)):
                promo = PromoCode(code=code_generator.promo_code(), amount=request.data["value_of_code"], active=True,
                                  event=event,
                                  radius=request.data["radius"])
                promo.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
