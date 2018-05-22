from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tokens.serializers.serializers import PromoCodeSerializer, EventSerializer, CodesCreateSerializer, \
    PromoCodeUpdateSerializer, PromoCodeRadiusUpdateSerializer
from tokens.mixins import LoginRequiredMixin, CreateListMixin
from rest_framework import authentication, permissions
from tokens.promo_codes import GeneratePromoCodes

# Create your views here.

from tokens.models import Events, PromoCode
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView


class ActivePromoCodesListApiView(LoginRequiredMixin, ListAPIView):
    queryset = PromoCode.objects.filter(active=True).order_by('-id')
    serializer_class = PromoCodeSerializer


class PromoCodesListApiView(LoginRequiredMixin, ListAPIView):
    queryset = PromoCode.objects.order_by('-id').all()

    serializer_class = PromoCodeSerializer


class PromoCodeUpdateApiView(LoginRequiredMixin, UpdateAPIView):
    queryset = PromoCode.objects.all()
    lookup_field = 'code'
    serializer_class = PromoCodeUpdateSerializer

    def perform_update(self, serializer):
        serializer.save()


class PromoCodeRetrieveApiView(LoginRequiredMixin, RetrieveAPIView):
    queryset = PromoCode.objects.all()
    lookup_field = 'code'
    serializer_class = PromoCodeSerializer

    def get(self, request, code, format=None, **kwargs):
        try:
            origin_lat = float(kwargs['origin_lat'])
            origin_lon = float(kwargs['origin_lon'])
            event_lon = PromoCode.objects.filter(code=code).get().event.lon
            event_lat = PromoCode.objects.filter(code=code).get().event.lat
            radius_from_event = GeneratePromoCodes.haversine(event_lon, event_lat, origin_lon, origin_lat)
            if radius_from_event < PromoCode.objects.filter(code=code).get().radius:

                return self.retrieve(PromoCode.objects.filter(code=code))
            else:
                return Response({"Error": "too far from event to use the promo code"},
                                status=status.HTTP_204_NO_CONTENT)

        except PromoCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PromoCodeRadiusUpdateApiView(LoginRequiredMixin, UpdateAPIView):
    queryset = PromoCode.objects.all()
    lookup_field = 'code'
    serializer_class = PromoCodeRadiusUpdateSerializer

    def perform_update(self, serializer):
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
            event = Events.objects.filter(name__exact=request.data["event"]).first()
            if not event:
                return Response({"Message": "associated event doesnt exist"}, status=status.HTTP_400_BAD_REQUEST)

            code_generator = GeneratePromoCodes()

            for i in range(int(number_of_promo_codes)):
                promo = PromoCode(code=code_generator.promo_code(), amount=request.data["value_of_code"], active=True,
                                  event=event,
                                  radius=request.data["radius"])
                promo.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
