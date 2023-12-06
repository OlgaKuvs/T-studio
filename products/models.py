from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=50)    
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)    
    description = models.TextField()   
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    rating = models.FloatField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.rating}"
