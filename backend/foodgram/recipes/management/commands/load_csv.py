import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes import models

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(settings.BASE_DIR, "static/data")

FILES_MODELS = {
    'ingredients.csv': models.Ingredients,
}


class Command(BaseCommand):
    help = "Загрузка данных из csv файлов."

    def handle(self, *args, **options):
        for file_name in FILES_MODELS:
            file_path = os.path.join(DATA_PATH, file_name)
            model = FILES_MODELS.get(file_name)
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        logger.info(model.objects.get_or_create(**row))
                    except Exception:
                        logger.error(file_path, model, row, exc_info=True)
