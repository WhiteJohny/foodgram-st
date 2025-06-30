from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    INGREDIENT_MAX_LENGTH = 100

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=INGREDIENT_MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=INGREDIENT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'measurement_unit'
                ],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    RECIPE_MAX_LENGTH = 100

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=RECIPE_MAX_LENGTH
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (минуты)',
        validators=[
            MinValueValidator(1),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient'
                ],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'
                ],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'
                ],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.recipe}'
