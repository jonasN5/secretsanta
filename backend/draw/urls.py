from django.urls import path, include
from rest_framework import routers

from draw.views import *

router = routers.SimpleRouter()
router.register('', ParticipantsViewSet)

urlpatterns = [
    path('participants/', include(router.urls)),  # Allow CRUD actions on User objects.
    path('draws/', DrawsView.as_view()),  # List all draws and create a new draw.
]
