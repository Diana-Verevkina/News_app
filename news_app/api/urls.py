from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import NewsViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', NewsViewSet, basename='news')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]