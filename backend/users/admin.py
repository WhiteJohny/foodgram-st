from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Subscription


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff'
    )
    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name'
    )
    ordering = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': (
            'first_name',
            'last_name',
            'username',
            'avatar'
        )}),
        ('Разрешения', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2'
            ),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'created')
    search_fields = (
        'user__username',
        'user__email',
        'author__username',
        'author__email'
    )
    list_filter = ('author',)
    autocomplete_fields = ('user', 'author')
    ordering = ('-created',)
    readonly_fields = ('created',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'author')

    def has_add_permission(self, request):
        # Запретить добавление через админку, если подписки управляются через API
        return False
