from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30)

class Category(models.Model):
    CategoryName = models.CharField(max_length=50)
    CategoryImage = models.FileField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except Exception as ex:
        print(ex)



# Product
class Product(models.Model):
    ProductName=models.CharField(max_length=50)
    ProductDescription = models.TextField()
    ProductCategory=models.IntegerField()
    ProductPrice=models.DecimalField(max_digits=12,decimal_places=2)
    ProductQty=models.IntegerField()
    ProductImage=models.FileField(upload_to="prod_uploads/")

# Cart
class Cart(models.Model):
    ProductID=models.IntegerField()
    ProductName=models.CharField(max_length=50)
    ProductPrice=models.DecimalField(max_digits=12,decimal_places=2)
    ProductQty=models.IntegerField()
    ProductTotal=models.DecimalField(decimal_places=2,max_digits=12)
    UserName=models.CharField(max_length=30)
    ProductImage=models.FileField(upload_to="prod_uploads/")

# Order
class Orders(models.Model):
    OrderDate = models.DateField(auto_now=True)
    UserName = models.CharField(max_length=30)
    OrderTotal = models.DecimalField(decimal_places=2, max_digits=12)
    Status = models.CharField(max_length=30)

# OrderItems
class OrdersItems(models.Model):
    OrderId = models.IntegerField()
    ProductID = models.IntegerField()
    ProductName = models.CharField(max_length=50)
    ProductPrice = models.DecimalField(max_digits=12, decimal_places=2)
    ProductQty = models.IntegerField()
    ProductTotal = models.DecimalField(decimal_places=2, max_digits=12)
