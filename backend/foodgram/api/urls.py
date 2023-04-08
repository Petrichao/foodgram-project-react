from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api import views

router_v1 = DefaultRouter()
router_v1.register(
    'tags',
    views.TagsViewSet,
    basename='tags'
)
router_v1.register(
    'ingredients',
    views.IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'recipes',
    views.RecipeViewSet,
    basename='recipes',
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]