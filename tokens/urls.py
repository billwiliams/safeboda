from django.conf.urls import url, include
from rest_framework import routers
from tokens.views import ActivePromoCodesListApiView
urlpatterns = [
    url(r'^api/active/tokens$', ActivePromoCodesListApiView.as_view(), name='list_active_tokens'),

]