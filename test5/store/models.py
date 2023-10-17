from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT, related_name='products')


