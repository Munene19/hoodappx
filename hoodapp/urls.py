from django.urls import include,path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import routers 
from .views import UserViewSet
router=routers.DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

userSignup=UserViewSet.as_view({
    'get':'list',
    'post':'create'
})

userLogin=UserViewSet.as_view({
    'get':'list',
    'post':'list'
})

userDetail=UserViewSet.as_view({
    'get':'retrieve'
})

urlpatterns = [
    path('',views.index),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', userSignup, name='user_signup'),
    path('auth/login/', userLogin, name='user_login'),
    path('auth/refresh-token/', refresh_jwt_token),
    path('users/<int:pk>/', userDetail, name='user-detail'),
    path('api/v1/', include(router.urls)),
    path('hoods/',views.HoodList.as_view()),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)