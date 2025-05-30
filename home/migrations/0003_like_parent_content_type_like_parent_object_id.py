# Generated by Django 5.1.3 on 2024-12-19 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('home', '0002_tag_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='parent_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_likes', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='like',
            name='parent_object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
