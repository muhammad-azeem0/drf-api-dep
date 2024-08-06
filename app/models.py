from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to='images/', blank=True, null= True)
    
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class WareHouse(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.TextField(null= False, blank=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name



class Stock(models.Model):
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.id)
    
    

class TransferStock(models.Model):
    
    from_warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='transfers_from')
    to_warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='transfers_to')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    class Status(models.TextChoices):
        RECIEVED = 'RE','Recieved'
        INTRANSIT = 'IN','Intransit'
        CANCELLED = 'CA','Cancelled'
        PROCESSING = 'PR','Processing'
        # PROCESSING is used to refer that choice in code
        # PR is database readable
        # Processing is human readable
        
    status = models.CharField(max_length=10, choices = Status.choices, default = Status.PROCESSING)
    
    
    