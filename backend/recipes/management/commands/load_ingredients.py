import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from JSON file into database'

    def handle(self, *args, **options):
        print(Ingredient.objects.count())

        file_path = os.path.join('data', 'ingredients.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ingredients = json.load(f)

                stats = {'created': 0, 'updated': 0, 'unchanged': 0}

                for item in ingredients:
                    obj, created = Ingredient.objects.update_or_create(
                        name=item['name'],
                        defaults={
                            'measurement_unit': item['measurement_unit']
                        }
                    )

                    if created:
                        stats['created'] += 1
                    elif obj.measurement_unit != item['measurement_unit']:
                        stats['updated'] += 1
                    else:
                        stats['unchanged'] += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Ingredients processed: "
                        f"{stats['created']} created, "
                        f"{stats['updated']} updated, "
                        f"{stats['unchanged']} unchanged"
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"File not found: {file_path}")
            )
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f"JSON decode error: {str(e)}")
            )
