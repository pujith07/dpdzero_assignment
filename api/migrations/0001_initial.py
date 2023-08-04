# Generated by Django 4.2.2 on 2023-08-03 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User_Data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("full_name", models.CharField(max_length=200)),
                ("age", models.PositiveIntegerField()),
                ("gender", models.CharField(max_length=10)),
            ],
        ),
    ]