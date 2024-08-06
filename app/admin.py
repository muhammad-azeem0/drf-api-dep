from django.contrib import admin
from .models import Product, WareHouse, TransferStock, Stock, User

admin.site.register(Product)
admin.site.register(WareHouse)
admin.site.register(TransferStock)
admin.site.register(Stock)
