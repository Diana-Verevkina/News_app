from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .ApiView import ApiView
from .views import CommentViewSet, FollowViewSet, NewsViewSet, ProfileViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', NewsViewSet, basename='news')
router_v1.register('profile', ProfileViewSet, basename='profile')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(r'news/(?P<news_id>\d+)/comments', CommentViewSet,
                   basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('swagger/', ApiView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
