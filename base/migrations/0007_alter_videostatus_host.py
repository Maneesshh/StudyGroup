# Generated by Django 4.2 on 2023-07-04 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_updated_videostatus_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videostatus',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
    ]