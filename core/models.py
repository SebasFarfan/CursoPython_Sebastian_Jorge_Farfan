from django.db import models

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50,blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    recommended_age= models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

class Book(models.Model):
    name= models.CharField(max_length=250, blank=False, null=False)
    age = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

class Partner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class BookLoan(models.Model):
    status = models.CharField(max_length=10, blank=False, null=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    date_loan = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)



    


