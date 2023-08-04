from django.db import models

# Create your models here.

class User_Data(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Stored_data(models.Model):
    key=models.CharField(max_length=100,unique=True)
    value=models.CharField(max_length=100)

    def __str__(self):
        return self.key