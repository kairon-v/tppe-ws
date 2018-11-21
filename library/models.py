from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11)

class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20)
    description = models.TextField()
    release_year = models.CharField(max_length=4)
    publisher = models.CharField(max_length=50)
    copies = models.IntegerField(default=0)
