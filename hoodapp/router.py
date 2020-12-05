from hood.views import PostViewSet, NeighborhoodViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', PostViewSet)

router = routers.DefaultRouter()
router.register('create_hood', NeighborhoodViewSet)