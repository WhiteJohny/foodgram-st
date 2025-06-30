import base64

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Subscription
from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для работы с изображениями в формате Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
            if data.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Размер изображения не должен превышать 10MB'
                )
        return super().to_internal_value(data)


class BaseRelationSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для отношений пользователь/рецепт."""

    class Meta:
        abstract = True
        fields = ['user', 'recipe']
        extra_kwargs = {
            'user': {'read_only': True},
            'recipe': {'required': True}
        }

    def get_already_exists_message(self):
        raise NotImplementedError(
            'Метод должен возвращать сообщение об ошибке'
        )

    def validate_recipe(self, value):
        user = self.context['request'].user
        model_class = self.Meta.model

        if model_class.objects.filter(user=user, recipe=value).exists():
            raise serializers.ValidationError(
                self.get_already_exists_message()
            )
        return value

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeMinifiedSerializer(recipe, context=self.context).data


class FavoriteSerializer(BaseRelationSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta(BaseRelationSerializer.Meta):
        model = Favorite

    def get_already_exists_message(self):
        return 'Рецепт уже в избранном'


class ShoppingCartSerializer(BaseRelationSerializer):
    """Сериализатор для списка покупок."""

    class Meta(BaseRelationSerializer.Meta):
        model = ShoppingCart

    def get_already_exists_message(self):
        return 'Рецепт уже в списке покупок'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'avatar'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return (
                request.build_absolute_uri(obj.avatar.url)
                if request else obj.avatar.url
            )
        return None

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    username = serializers.CharField(
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
            UniqueValidator(queryset=User.objects.all())
        ],
        max_length=150
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class UserWithRecipesSerializer(UserSerializer):
    """Сериализатор для пользователя с рецептами."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes', 'recipes_count']

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeMinifiedSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        if self.context.get('is_subscriptions_list'):
            return True

        return Subscription.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    class Meta:
        model = Subscription
        fields = ('user', 'author')
        extra_kwargs = {
            'user': {'read_only': True},
            'author': {'required': True}
        }

    def validate_author(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscription.objects.filter(user=user, author=value).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        return value


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор для рецептов."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return (
                request.build_absolute_uri(obj.image.url)
                if request else obj.image.url
            )
        return None


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    """Основной сериализатор для рецептов."""
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_amounts',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return (
                request.build_absolute_uri(obj.image.url)
                if request else obj.image.url
            )
        return None

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.in_shopping_cart.filter(user=user).exists()
        return False


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецептов."""
    ingredients = serializers.JSONField(required=True, write_only=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'ingredients', 'image',
            'name', 'text', 'cooking_time'
        ]
        read_only_fields = ['id']

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходим хотя бы один ингредиент'
            )

        for item in value:
            if 'id' not in item or 'amount' not in item:
                raise serializers.ValidationError(
                    'Каждый ингредиент должен содержать "id" и "amount"'
                )

        ingredient_ids = [item['id'] for item in value]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )

        existing_ids = set(Ingredient.objects.filter(
            id__in=ingredient_ids
        ).values_list('id', flat=True))

        missing_ids = set(ingredient_ids) - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f'Ингредиенты с ID {", ".join(map(str, missing_ids))}'
                ' не существуют'
            )

        for item in value:
            amount = item['amount']
            if not isinstance(amount, int):
                if not str(amount).isdigit():
                    raise serializers.ValidationError(
                        f'Количество ингредиента ID {item["id"]}'
                        ' должно быть целым числом больше 0'
                    )
                amount = int(amount)
            if amount < 1:
                raise serializers.ValidationError(
                    f'Количество ингредиента ID {item["id"]}'
                    ' должно быть целым числом больше 0'
                )

        return value

    def validate(self, data):
        cooking_time = data.get('cooking_time')
        if cooking_time and cooking_time < 1:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно'
                                ' быть не менее 1 минуты'
            })

        if self.context['request'].method == 'POST':
            if 'image' not in data:
                raise serializers.ValidationError({
                    'image': 'Это поле обязательно при создании рецепта'
                })

        if self.context['request'].method == 'PATCH':
            required_fields = [
                'ingredients', 'name', 'text', 'cooking_time'
            ]
            missing_fields = [
                field for field in required_fields if field not in data
            ]

            if missing_fields:
                raise serializers.ValidationError({
                    'required_fields': 'При обновлении обязательны поля: '
                                       f'{", ".join(missing_fields)}'
                })

        return data

    def create_ingredients(self, recipe, ingredients):
        objs = []
        for ingredient in ingredients:
            objs.append(RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=int(ingredient['amount'])
            ))
        RecipeIngredient.objects.bulk_create(objs)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)

        if ingredients is not None:
            instance.ingredient_amounts.all().delete()
            self.create_ingredients(instance, ingredients)

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class SetAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления аватара."""
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']


class SetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ShortCodeValidatorSerializer(serializers.Serializer):
    """Сериализатор для короткой ссылки рецепта."""

    short_code = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.recipe_queryset = kwargs.pop(
            'recipe_queryset', Recipe.objects.all()
        )
        super().__init__(*args, **kwargs)

    def validate_short_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('Неверный формат ссылки')

        recipe_id = int(value)

        if not self.recipe_queryset.filter(pk=recipe_id).exists():
            raise serializers.ValidationError('Рецепт не найден')

        return recipe_id
