from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class category(models.TextChoices):
    COPMUTERS = 'Computers'
    FOOD = 'Food'
    KIDS = 'Kids'
    HOME = 'Home'


class Product(models.Model):
    def __str__(self):
        return  self.name

    name = models.CharField(max_length=200,default="",blank=False)
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand = models.CharField(max_length=200,default="",blank=False)
    category = models.CharField(max_length=40,choices=category.choices)
    ratings = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)





class Review(models.Model):
    def __str__(self):
        return  self.comment
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE,related_name="reviews")
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000,default="",blank=False)
    createAt = models.DateTimeField(auto_now_add=True)
