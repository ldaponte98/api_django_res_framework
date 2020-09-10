from django.contrib import admin
from .models import Client, Category, Product, Purchase, PurchaseDetail, Store, StoreManager
# Register your models here.

admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
admin.site.register(Store)
admin.site.register(StoreManager)
