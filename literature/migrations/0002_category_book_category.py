# Generated by Django 5.1.3 on 2024-12-20 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('literature', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='cbook', to='literature.category'),
        ),
    ]
