# Generated by Django 4.0.6 on 2022-11-20 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_review_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.CharField(choices=[('+', 'Положительный'), ('-', 'Отрицательный')], max_length=50),
        ),
    ]