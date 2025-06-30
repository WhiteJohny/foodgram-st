import pytest

from rest_framework import status

from users.models import User
from recipes.models import (
    Recipe,
    RecipeIngredient,
    Ingredient,
    Favorite,
    ShoppingCart
)


@pytest.mark.django_db
def test_recipe_add_to_favorite(client):
    # Создаем пользователя и рецепт
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    recipe = Recipe.objects.create(
        author=user,
        name='Рецепт 1',
        text='Описание',
        cooking_time=30
    )

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Добавляем в избранное
    response = client.post(f'/api/recipes/{recipe.id}/favorite/')
    assert response.status_code == status.HTTP_201_CREATED
    assert Favorite.objects.filter(user=user, recipe=recipe).exists()


@pytest.mark.django_db
def test_recipe_remove_from_favorite(client):
    # Создаем пользователя и рецепт
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    recipe = Recipe.objects.create(
        author=user,
        name='Рецепт 1',
        text='Описание',
        cooking_time=30
    )
    Favorite.objects.create(user=user, recipe=recipe)

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Удаляем из избранного
    response = client.delete(f'/api/recipes/{recipe.id}/favorite/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Favorite.objects.filter(id=response.data).exists()


@pytest.mark.django_db
def test_recipe_add_to_shopping_cart(client):
    # Создаем пользователя и рецепт
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    recipe = Recipe.objects.create(
        author=user,
        name='Рецепт 1',
        text='Описание',
        cooking_time=30
    )

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Добавляем в список покупок
    response = client.post(f'/api/recipes/{recipe.id}/shopping_cart/')
    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingCart.objects.filter(user=user, recipe=recipe).exists()


@pytest.mark.django_db
def test_recipe_remove_from_shopping_cart(client):
    # Создаем пользователя и рецепт
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    recipe = Recipe.objects.create(
        author=user,
        name='Рецепт 1',
        text='Описание',
        cooking_time=30
    )
    ShoppingCart.objects.create(user=user, recipe=recipe)

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Удаляем из списка покупок
    response = client.delete(f'/api/recipes/{recipe.id}/shopping_cart/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ShoppingCart.objects.filter(user=user, recipe=recipe).exists()
