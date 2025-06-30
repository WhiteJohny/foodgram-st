import pytest

from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Recipe
from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_user_subscriptions(client):
    # Создаем пользователей
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )
    author = User.objects.create_user(
        email='author@example.com',
        username='author',
        password='Qwerty123'
    )
    Recipe.objects.create(
        author=author,
        name='Рецепт 1',
        text='Описание',
        cooking_time=30
    )
    Recipe.objects.create(
        author=author,
        name='Рецепт 2',
        text='Еще рецепт',
        cooking_time=45
    )

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'user@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Подписываемся
    response = client.post(f'/api/users/{author.id}/subscribe/')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['recipes_count'] == 2
    assert len(response.data['recipes']) == 2
