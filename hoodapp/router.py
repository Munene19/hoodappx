from hood.views import PostViewSet, NeighborhoodViewSet, BusinessViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', PostViewSet)

router.register('create_hood', NeighborhoodViewSet)

router.register('market', BusinessViewSet)