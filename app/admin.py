from django.contrib import admin
from .models import Product, WareHouse, TransferStock, Stock
from django.contrib.auth.models import User

# Custom admin class for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_price', 'sale_price')
    # search_fields = ('name',)

# Custom admin class for WareHouse
class WareHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager')
    # search_fields = ('name', 'address')

# Custom admin class for TransferStock
class TransferStockAdmin(admin.ModelAdmin):
    list_display = ('from_warehouse', 'to_warehouse', 'user', 'product', 'quantity', 'status')
    # search_fields = ('from_warehouse__name', 'to_warehouse__name', 'product__name', 'user__username')


# Custom admin class for Stock
class StockAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'quantity')
    # search_fields = ('warehouse__name', 'product__name')


admin.site.register(Product, ProductAdmin)
admin.site.register(WareHouse, WareHouseAdmin)
admin.site.register(TransferStock, TransferStockAdmin)
admin.site.register(Stock, StockAdmin)
