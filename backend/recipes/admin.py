from django.contrib import admin
from django.db.models import Count

from .models import (
    Ingredient, Recipe, RecipeIngredient,
    Favorite, ShoppingCart
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
        'recipe_count'
    )
    search_fields = ('name', )
    ordering = ('name', )
    fields = ('name', 'measurement_unit')
    search_help_text = 'Поиск по названию ингредиента'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            recipe_count=Count('recipe_ingredients')
        )

    def recipe_count(self, obj):
        return obj.recipe_ingredients.count()

    recipe_count.short_description = 'Используется в рецептах'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    autocomplete_fields = ('ingredient', )
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        formset.form.base_fields['ingredient'].label_from_instance = (
            lambda inst: f'{inst.name} ({inst.measurement_unit})'
        )
        return formset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'cooking_time',
        'pub_date',
        'favorites_count'
    )
    search_fields = ('name', 'author__username', 'author__email')
    search_help_text = 'Поиск по названию, имени автора или email'
    list_filter = ('pub_date', 'cooking_time')
    inlines = (RecipeIngredientInline, )
    autocomplete_fields = ('author',)
    readonly_fields = ('pub_date', 'favorites_count')

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('author')
            .prefetch_related('ingredient_amounts')
            .annotate(_favorites_count=Count('favorited_by'))
        )

    def favorites_count(self, obj):
        return obj._favorites_count

    favorites_count.admin_order_field = '_favorites_count'
    favorites_count.short_description = 'В избранном'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
        'recipe__author__username'
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('user', 'recipe__author')
        )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
        'recipe__author__username'
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('user', 'recipe__author')
        )
