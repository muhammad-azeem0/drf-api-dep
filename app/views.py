from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product, WareHouse, TransferStock, Stock
from .serializers import ProductSerializer, WareHouseSerializer, TransferStockSerializer, StockSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.db.models import F
from django.db import transaction
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
    
    def get_objects(self, pk):
        try:
            return WareHouse.objects.select_related('manager').get(pk=pk)
        except WareHouse.DoesNotExist:
            return None
        
    def list(self, request):
        objs = WareHouse.objects.select_related('manager').all()
        serializer = WareHouseSerializer(objs, many = True) 
        return Response(serializer.data)
    
   
    def retrieve(self, request, pk = None):
        # obj = WareHouse.objects.select_related('manager').get(id=pk)
        obj = self.get_objects(pk)
        if obj is not None:
            serializer = WareHouseSerializer(obj)
            return Response(serializer.data)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
   
   
    def create(self, request):
        data = request.data
        serializer = WareHouseSerializer(data = data)
        if serializer.is_valid():
            serializer.save(manager = request.user)
            return Response({'msg':'Data Created !!'})
        return Response(serializer.errors)
   
   
    def update(self, request, pk):
        # id = pk
        # obj = WareHouse.objects.select_related('manager').get(pk=id)
        obj = self.get_objects(pk)
        
        if obj is not None:
            serializer = WareHouseSerializer(obj, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Complete Data Updated !!'})
            return Response(serializer.errors)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
   
    def partial_update(self, request, pk):
        # id = pk
        # stu = WareHouse.objects.select_related('manager').get(pk=id)
        obj = self.get_objects(pk)
        
        if obj is not None:
            serializer = WareHouseSerializer(obj, data = request.data, partial = True)
                
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial Data Updated !!'})
            return Response(serializer.errors)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

   
    def destroy(self, request, pk):
        # id = pk 
        # stu = WareHouse.objects.select_related('manager').get(pk=id)
        obj = self.get_objects(pk)
        
        if obj is not None:
            obj.delete()
            return Response({'msg':'Data Deleted !!'})
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
   
   

# ---------------------------------------------------------TransferStock model CRUD----------------------------------------------------------

class TransferStockViewset(viewsets.ViewSet):
    
    def get_object(self, pk):
        try:
            return TransferStock.objects.select_related('from_warehouse','to_warehouse', 'user', 'product').get(pk=pk)
        except TransferStock.DoesNotExist:
            return None
            
    
    def list(self, request):
        queryset = TransferStock.objects.select_related('from_warehouse','to_warehouse', 'user', 'product').all()
        serializer = TransferStockSerializer(queryset, many = True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = TransferStockSerializer(obj)
            return Response(serializer.data)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # # create function without transaction atomic
    # def create(self, request):
    #     serializer = TransferStockSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg':'Data Created !!'})
    #     return Response(serializer.errors)
    
    
    def create(self, request):
        serializer = TransferStockSerializer(data=request.data)
        if serializer.is_valid():
            from_warehouse_id = serializer.validated_data['from_warehouse'].id
            to_warehouse_id = serializer.validated_data['to_warehouse'].id
            product_id = serializer.validated_data['product'].id
            quantity = serializer.validated_data['quantity']
            
            if from_warehouse_id != to_warehouse_id:
                try:
                    with transaction.atomic():
                        # Check if stock exists in the source warehouse and if there's enough quantity
                        stock_from_warehouse = Stock.objects.get(warehouse_id=from_warehouse_id, product_id=product_id)
                        
                        if stock_from_warehouse.quantity < quantity:
                            return Response({'error': 'Insufficient stock in the source warehouse.'},status=status.HTTP_400_BAD_REQUEST)
                        
                        # Deduct quantity from the source warehouse
                        stock_from_warehouse.quantity -= quantity
                        stock_from_warehouse.save()
                        
                        # Get or create stock in the destination warehouse
                        stock_to_warehouse, created = Stock.objects.get_or_create(
                            warehouse_id=to_warehouse_id,
                            product_id=product_id,
                            defaults={'quantity': 0}
                        )
                        
                        # Add quantity to the destination warehouse
                        stock_to_warehouse.quantity += quantity
                        stock_to_warehouse.save()
                        
                        # Save the transfer record

                        #serializer.save(status=TransferStock.Status.INTRANSIT)
                        serializer.save(user=request.user)
                        
                    return Response({'msg': 'Stock transferred successfully'},status=status.HTTP_201_CREATED)
                
                except Stock.DoesNotExist:
                    return Response(
                        {'error': 'Stock entry not found in the source warehouse.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                except Exception as e:
                    return Response(
                        {'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    {'error': 'Source and destination warehouses are the same.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    def update(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = TransferStockSerializer(obj, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Complete Data Updated !!'})
            return Response(serializer.errors)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    def partial_update(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = TransferStockSerializer(obj, data = request.data, partial = True)
                
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial Data Updated !!'})
            return Response(serializer.errors)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

   
    def destroy(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            obj.delete()
            return Response({'msg':'Data Deleted !!'})
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
# ---------------------------------------------------------Stok model CRUD----------------------------------------------------------

class StockViewset(viewsets.ViewSet):
    
    def get_object(self, pk):
        try:
            return Stock.objects.select_related('warehouse', 'product').get(pk=pk)
        except Stock.DoesNotExist:
            return None
        
    
    def list(self, request):
        queryset = Stock.objects.select_related('warehouse', 'product').annotate(
            name = F('warehouse__name')
            ).all()
        serializer = StockSerializer(queryset, many = True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = StockSerializer(obj)
            return Response(serializer.data)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # # simple create function without transaction atomicity
    def create(self, request):
        serializer = StockSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created !!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    
    
    
    def update(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = StockSerializer(obj, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Complete Data Updated !!'})
            return Response(serializer.errors)
        
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    def partial_update(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            serializer = StockSerializer(obj, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'partial Data Updated !!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

   
    def destroy(self, request, pk):
        obj = self.get_object(pk)
        
        if obj is not None:
            obj.delete()
            return Response({'msg':'Data Deleted !!'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)