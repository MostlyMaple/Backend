from django.db import models
from django.contrib.auth.models import User

class DiscountCode(models.Model):
    name = models.CharField(max_length=200)
    discount = models.FloatField(default=0, null=True, blank=True)
    def __str__(self):
        return self.name

class Item(models.Model):
    topic = models.CharField(max_length=200, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='640x360.png')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.item_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    shippingPrice = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    totalPrice = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    isPaid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    image = models.ImageField(null=True, blank=True, default='640x360.png')

    def __str__(self):
        return str(self.name)

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.address)
