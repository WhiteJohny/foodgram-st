import pytest

from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Recipe

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_recipes_list(client):
    # Создаем пользователей и рецепты
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    Recipe.objects.create(
        author=user,
        name='Рецепт 1',
        text='Описание рецепта 1',
        cooking_time=30
    )
    Recipe.objects.create(
        author=user,
        name='Рецепт 2',
        text='Описание рецепта 2',
        cooking_time=45
    )

    response = client.get('/api/recipes/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_recipe_create_with_invalid_data(client):
    # Создаем пользователя
    User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Попытка создания рецепта без обязательных полей
    data = {
        "name": "Без ингредиентов",
        "text": "Нет ингредиентов",
        "cooking_time": 30
    }
    response = client.post('/api/recipes/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'ingredients' in response.data


@pytest.mark.django_db
def test_recipe_delete(client):
    # Создаем пользователя и рецепт
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    recipe = Recipe.objects.create(
        author=user,
        name='Удалить меня',
        text='Тестовый рецепт',
        cooking_time=30
    )

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Удаляем рецепт
    response = client.delete(f'/api/recipes/{recipe.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Recipe.objects.filter(id=recipe.id).exists()
