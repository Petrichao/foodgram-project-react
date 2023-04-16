# Generated by Django 3.2 on 2023-04-15 16:09

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipes_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measurement_unit',
            field=models.CharField(default=123, max_length=10, verbose_name='Единица измерения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='cooking_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingrediet'),
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
