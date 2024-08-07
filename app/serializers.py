from rest_framework import serializers
from .models import Product, WareHouse, TransferStock, Stock


class ProductSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Product
        fields = '__all__'
        
class WareHouseSerializer(serializers.ModelSerializer): 
    class Meta:
        model = WareHouse
        #fields = '__all__'
        fields = ['id', 'name', 'address', 'manager']
        # read_only_fields = ['manager']
        
        
class StockSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    class Meta:
        model = Stock
        # fields = '__all__'
        fields = ['id', 'warehouse', 'product','quantity', 'name']



class TransferStockSerializer(serializers.ModelSerializer): 
    class Meta:
        model = TransferStock
        fields = '__all__'
        
        
