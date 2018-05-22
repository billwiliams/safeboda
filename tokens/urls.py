from django.conf.urls import url, include
from rest_framework import routers
from tokens.views import ActivePromoCodesListApiView, PromoCodesList

urlpatterns = [
    url(r'^api/active/promo/codes$', ActivePromoCodesListApiView.as_view(), name='list_active_tokens'),
    url(r'^api/promo/codes/generate$', PromoCodesList.as_view(), name='generate_tokens'),

]
