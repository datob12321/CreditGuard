from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='cards')

urlpatterns = [
    path('', include(router.urls))
    # path('', views.CardViewSet.as_view({'get': 'list', 'post': 'create'}), name='cards'),
    # path('create', views.CardViewSet.as_view({'post': 'create'}), name='create')
]
