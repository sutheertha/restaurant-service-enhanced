from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_confirmed = models.BooleanField(default=False)
    
    def update_total(self):
        self.total = sum(item.price for item in self.cartitem_set.all())
        self.save()

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def update_total(self):
        self.total = sum(item.price for item in self.cartitem_set.all())
        self.save()

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

