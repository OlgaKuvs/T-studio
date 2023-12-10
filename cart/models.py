from django.db import models

class Shipping(models.Model):
    order_weight = models.IntegerField(null=True, blank=True)
    postal_rates = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.order_weight}, {self.postal_rates}"
    
    class Meta:
        verbose_name_plural = 'Shipping'