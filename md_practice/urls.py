
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from app import views
from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()

router.register('productapi', views.productViewSet, basename='productapi')
router.register('wareapi', views.WareHouseViewSet, basename='wareapi')
router.register('transferapi', views.TransferStockViewset, basename='transferapi')
router.register('stockapi', views.StockViewset, basename='stockapi')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include(router.urls)),
    
]+ debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)