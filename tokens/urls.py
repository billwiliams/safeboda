from django.conf.urls import url, include
from rest_framework import routers
from tokens.views import ActivePromoCodesListApiView, PromoCodesList, EventCreateApiView, PromoCodesListApiView, \
    PromoCodeUpdateApiView, PromoCodeRadiusUpdateApiView

urlpatterns = [
    url(r'^api/active/promo/codes$', ActivePromoCodesListApiView.as_view(), name='list_active_tokens'),
    url(r'^api/list/promo/codes$', PromoCodesListApiView.as_view(), name='list_all_tokens'),
    url(r'^api/promo/codes/generate$', PromoCodesList.as_view(), name='generate_tokens'),
    url(r'^api/events/create$', EventCreateApiView.as_view(), name='create_event'),
    url(r'^api/(?P<code>.*)/deactivate$', PromoCodeUpdateApiView.as_view(), name='deactivate_code'),
    url(r'^api/(?P<code>.*)/radius/update', PromoCodeRadiusUpdateApiView.as_view(), name='deactivate_code'),

]
