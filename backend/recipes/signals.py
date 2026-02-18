from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Recipe
from .tasks import publish_task


@receiver(post_save, sender=Recipe)
def recipe_post_save(sender, instance, created, **kwargs):
    if created:
        print(f" [x] Recipe created: {instance}")
        publish_task('foodish', instance.id)
        publish_task('nyt', instance.id)
