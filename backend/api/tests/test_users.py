import pytest

from rest_framework import status

from users.models import User, Subscription


@pytest.mark.django_db
def test_user_registration(client):
    data = {
        "email": "new_user@example.com",
        "username": "new_user",
        "first_name": "Иван",
        "last_name": "Иванов",
        "password": "Qwerty123"
    }
    response = client.post('/api/users/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email='new_user@example.com').exists()


@pytest.mark.django_db
def test_user_duplicate_username(client):
    # Создаем пользователя
    User.objects.create_user(
        email='user@example.com',
        username='user',
        password='Qwerty123'
    )

    # Пытаемся создать пользователя с тем же username
    data = {
        "email": "another@example.com",
        "username": "user",
        "first_name": "Петр",
        "last_name": "Петров",
        "password": "Qwerty123"
    }
    response = client.post('/api/users/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data


@pytest.mark.django_db
def test_subscribe_to_author(client):
    # Создаем пользователей
    user = User.objects.create_user(
        email='subscriber@example.com',
        username='subscriber',
        password='Qwerty123'
    )
    author = User.objects.create_user(
        email='author@example.com',
        username='author',
        password='Qwerty123'
    )

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'subscriber@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Подписываемся
    response = client.post(f'/api/users/{author.id}/subscribe/')
    assert response.status_code == status.HTTP_201_CREATED
    assert Subscription.objects.filter(user=user, author=author).exists()


@pytest.mark.django_db
def test_unsubscribe_from_author(client):
    # Создаем пользователей
    user = User.objects.create_user(
        email='subscriber@example.com',
        username='subscriber',
        password='Qwerty123'
    )
    author = User.objects.create_user(
        email='author@example.com',
        username='author',
        password='Qwerty123'
    )
    Subscription.objects.create(user=user, author=author)

    # Авторизуемся
    response = client.post('/api/auth/token/login/', {
        'email': 'subscriber@example.com',
        'password': 'Qwerty123'
    })
    token = response.data['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    # Отписываемся
    response = client.delete(f'/api/users/{author.id}/subscribe/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Subscription.objects.filter(user=user, author=author).exists()


@pytest.mark.django_db
def test_user_avatar_upload(client):
    # Создаем пользователя
    user = User.objects.create_user(
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

    # Загружаем аватар
    data = {
        "avatar": "data:image/png;base64,iVBORw0KGgoAAAA"
                  "NSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBM"
                  "VEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EA"
                  "AAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByx"
                  "OyYQAAAABJRU5ErkJggg=="
    }
    response = client.put('/api/users/me/avatar/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'avatar' in response.data
    assert 'default.jpg' not in response.data['avatar']


@pytest.mark.django_db
def test_user_avatar_delete(client):
    # Создаем пользователя
    user = User.objects.create_user(
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

    # Удаляем аватар
    response = client.delete('/api/users/me/avatar/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
