from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11)

class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(unique=True, max_length=20)
    description = models.TextField()
    release_year = models.CharField(max_length=4)
    publisher = models.CharField(max_length=50)
    copies = models.IntegerField(default=0)

class BookLoan(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	loan_date = models.DateField(auto_now=True)
	days = models.IntegerField(default=0)
	return_date = models.DateField(null=True)

