# Generated by Django 3.2.8 on 2021-10-28 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_favoriteproject_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]