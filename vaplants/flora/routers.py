
from rest_framework import routers
from .views import UserViewSet

router = routers.SimpleRouter(railing_slash=False)
router.register(r'users', UserViewSet)

