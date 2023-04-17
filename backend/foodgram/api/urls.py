from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views as a_views
from users import views as u_views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'tags',
    a_views.TagsViewSet,
    basename='tags'
)
router_v1.register(
    'ingredients',
    a_views.IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    'recipes',
    a_views.RecipeViewSet,
    basename='recipes',
)
router_v1.register(
    'users',
    u_views.CustomUserViewSet,
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
