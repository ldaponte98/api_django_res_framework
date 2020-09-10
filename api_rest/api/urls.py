from django.urls import path
from . import views

urlpatterns = [
    #paths users
    path('user-create/', views.userCreate, name = "user_create"),

    #paths categories
    path('categories/', views.categoryList, name = "categories"),
    path('category-search/<int:pk>', views.categorySearch, name = "category_search"),
    path('category-create/', views.categoryCreate, name = "category_create"),
    path('category-edit/<int:pk>', views.categoryEdit, name = "category_edit"),

    #paths shops
    path('shops/', views.storeList, name = "shops"),
    path('store-search/<int:pk>', views.storeSearch, name = "store_search"),
    path('store-create/', views.storeCreate, name = "store_create"),
    path('store-edit/<int:pk>', views.storeEdit, name = "store_edit"),

    #paths products
    path('products/', views.productList, name = "products"),
    path('catalog/', views.productCatalog, name = "product_catalog"),
    path('catalog-find/<int:pk>', views.productCatalogFindStore, name = "product_catalog_find"),
    path('product-search/<int:pk>', views.productSearch, name = "product_search"),
    path('product-create/', views.productCreate, name = "product_create"),
    path('product-edit/<int:pk>', views.productEdit, name = "product_edit"),
    path('product-delete/<int:pk>', views.productDelete, name = "product_delete"),

    #paths purchases 
    path('purchases', views.purchaseList, name = "purchase_list"),
    path('purchase-create/', views.purchaseCreate, name = "purchase_create"),
    path('purchase-history-client/<int:pk>', views.purchaseHistoryClient, name = "purchase_history_client"),
]