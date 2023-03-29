from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TagsViewSet, IngredientsViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router_v1.urls)),
]
