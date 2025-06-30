import pytest

from rest_framework import status

from recipes.models import Ingredient


@pytest.mark.django_db
def test_ingredients_list(client):
    # Создаем ингредиенты
    Ingredient.objects.create(name='Сахар', measurement_unit='грамм')
    Ingredient.objects.create(name='Молоко', measurement_unit='миллилитр')

    response = client.get('/api/ingredients/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_ingredients_filter_by_name(client):
    # Создаем ингредиенты
    Ingredient.objects.create(name='сахар', measurement_unit='грамм')
    Ingredient.objects.create(name='соль', measurement_unit='грамм')

    response = client.get('/api/ingredients/?name=сах')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'сахар'
