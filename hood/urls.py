from django.urls import include,path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import routers 
from .views import UserViewSet
from knox import views as knox_views
from .views import LoginAPI, hoodDetail
from django.views.decorators.csrf import csrf_exempt

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
    path('', views.index),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', userSignup, name='user_signup'),
    path('auth/login/', userLogin, name='user_login'),
    path('joinhood/', views.joinhood, name='join_hood'),
    # path('auth/refresh-token/', refresh_jwt_token),
    path('users/<int:pk>/', userDetail, name='user-detail'),
    path('api/v1/', include(router.urls)),
    path('hoods/',views.HoodList.as_view()),
    # path('api/v1/post/',views.PostList.as_view()),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/v1/view_hood/<str:pk>/', views.hoodDetail, name='hood-info'),
    # path('api/v1/profile/', csrf_exempt(views.CreatePost.as_view), name='post-create'),
    # path('api/hoodcreate/', views.hoodCreate, name='hood-create')
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


