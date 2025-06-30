from django.urls import path, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet, RecipeViewSet,
    IngredientViewSet,
    RecipeShortLinkView,
    RecipeShortRedirectView
)

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),

    path(
        'api/recipes/<int:pk>/get-link/',
        RecipeShortLinkView.as_view(),
        name='recipe-short-link'
    ),
    path(
        'r/<str:short_code>/',
        RecipeShortRedirectView.as_view(),
        name='recipe-redirect'
    ),
]
