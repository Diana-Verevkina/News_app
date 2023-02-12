from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import NewsViewSet, ProfileViewSet, CommentViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', NewsViewSet, basename='news')
router_v1.register('profile', ProfileViewSet, basename='profile')
router_v1.register(r'news/(?P<news_id>\d+)/comments', CommentViewSet,
                   basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]