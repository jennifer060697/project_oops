# Generated by Django 4.1.5 on 2023-02-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_search_alter_stores_star'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchWithFeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='CONTENT')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='CREATE_DATE')),
                ('thumbs', models.BooleanField(verbose_name='THUMBS')),
            ],
        ),
    ]
