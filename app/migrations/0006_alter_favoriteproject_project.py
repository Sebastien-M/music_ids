# Generated by Django 3.2.8 on 2021-10-28 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_miduser_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='app.project'),
        ),
    ]
