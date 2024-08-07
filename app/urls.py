from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('product', views.productViewSet, basename='product')
router.register('warehouse', views.WareHouseViewSet, basename='warehouse')
router.register('transferstock', views.TransferStockViewset, basename='transferstock')
router.register('stock', views.StockViewset, basename='stockapi')

urlpatterns = [
    path('', include(router.urls)),
]
