# products/models.py
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('service', 'Service'),
        ('hardware', 'Hardware'),
        ('software', 'Software'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    product_image=models.ImageField(upload_to='product_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
