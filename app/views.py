from django.shortcuts import render
from .models import Product, WareHouse, TransferStock, Stock
from .serializers import ProductSerializer, WareHouseSerializer, TransferStockSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

# Create your views here.


# ---------------------------------------------------------Product model CRUD---------------------------------------------------------

class productViewSet(viewsets.ViewSet):
    
    def list(self, request):
        objs = Product.objects.all()
        serializer = ProductSerializer(objs, many = True) 
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk = None):
        obj = Product.objects.get(id=pk)
        serializer = ProductSerializer(obj)
        return Response(serializer.data)
    
        
    def create(self, request):
        data = request.data
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created !!'})
        return Response(serializer.errors)
    
    
    def update(self, request, pk):
        id = pk
        stu = Product.objects.get(pk=id)
        serializer = ProductSerializer(stu, data = request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated !!'})
        return Response(serializer.errors)
        
    
    def partial_update(self, request, pk):
        id = pk
        stu = Product.objects.get(pk=id)
        serializer = ProductSerializer(stu, data = request.data, partial = True)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial Data Updated !!'})
        return Response(serializer.errors)

   
    def destroy(self, request, pk):
        id = pk 
        stu = Product.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data Deleted !!'})
   




# ---------------------------------------------------------WareHouse model CRUD----------------------------------------------------------

class WareHouseViewSet(viewsets.ViewSet):
    
    def list(self, request):
        objs = WareHouse.objects.all()
        serializer = WareHouseSerializer(objs, many = True) 
        return Response(serializer.data)
    
   
    def retrieve(self, request, pk = None):
        obj = WareHouse.objects.get(id=pk)
        serializer = WareHouseSerializer(obj)
        return Response(serializer.data)
   
       
    def create(self, request):
        data = request.data
        serializer = WareHouseSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created !!'})
        return Response(serializer.errors)
   
   
    def update(self, request, pk):
        id = pk
        stu = WareHouse.objects.get(pk=id)
        serializer = WareHouseSerializer(stu, data = request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated !!'})
        return Response(serializer.errors)
    
   
    def partial_update(self, request, pk):
        id = pk
        stu = WareHouse.objects.get(pk=id)
        serializer = WareHouseSerializer(stu, data = request.data, partial = True)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial Data Updated !!'})
        return Response(serializer.errors)

   
    def destroy(self, request, pk):
        id = pk 
        stu = WareHouse.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data Deleted !!'})
   
   

# ---------------------------------------------------------TransferStock model CRUD----------------------------------------------------------

class TransferStockViewset(viewsets.ViewSet):
    
    def list(self, request):
        queryset = TransferStock.objects.all()
        serializer = TransferStockSerializer(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        queryset = TransferStock.objects.get(pk = id)
        serializer = TransferStockSerializer(queryset)
        
        return Response(serializer.data)
    
    
    def create(self, request):
        serializer = TransferStockSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created !!'})
        return Response(serializer.errors)
    
    
    def update(self, request, pk):
        id = pk
        obj = TransferStock.objects.get(pk = id)
        serializer = TransferStockSerializer(obj, data= request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated !!'})
        return Response(serializer.errors)
    
    
    def partial_update(self, request, pk):
        id = pk
        stu = TransferStock.objects.get(pk=id)
        serializer = TransferStockSerializer(stu, data = request.data, partial = True)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial Data Updated !!'})
        return Response(serializer.errors)

   
    def destroy(self, request, pk):
        id = pk 
        stu = TransferStock.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data Deleted !!'})
    
    
    
    
# ---------------------------------------------------------Stok model CRUD----------------------------------------------------------

class StockViewset(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Stock.objects.all()
        serializer = StockSerializer(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        queryset = Stock.objects.get(pk = id)
        serializer = StockSerializer(queryset)
        
        return Response(serializer.data)
    
    
    def create(self, request):
        serializer = StockSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created !!'})
        return Response(serializer.errors)
    
    
    def update(self, request, pk):
        id = pk
        obj = Stock.objects.get(pk = id)
        serializer = StockSerializer(obj, data= request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated !!'})
        return Response(serializer.errors)
    
    
    def partial_update(self, request, pk):
        id = pk
        stu = Stock.objects.get(pk=id)
        serializer = StockSerializer(stu, data = request.data, partial = True)
            
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial Data Updated !!'})
        return Response(serializer.errors)

   
    def destroy(self, request, pk):
        id = pk 
        stu = Stock.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data Deleted !!'})