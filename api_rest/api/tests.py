import json

from api.serializers import UserSerializer
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Client, Category, Product, Purchase, PurchaseDetail, Store, StoreManager


class StoreTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin123", password="admin123", is_superuser=1)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
    
    def test_create_store(self):
        data = {
            "name" : "Pintuco",
            "document" : "153087"
        }
        response = self.client.post("/api/1.0/store-create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_auth_not_create_store(self):
        self.client.force_authenticate(user=None)
        data = {
            "name" : "Pintuco",
            "document" : "153087"
        }
        response = self.client.post("/api/1.0/store-create/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_store(self):

        data = {
            "name" : "Pintuco max",
            "document" : "153087"
        }
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        response = self.client.post("/api/1.0/store-edit/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_store(self):
        
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store = Store.objects.create(name="Pinturas Mari", document="23557786767-7")
        response = self.client.get("/api/1.0/shops/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_store(self):
        
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        response = self.client.get("/api/1.0/store-search/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin123", password="admin123", is_superuser=1)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
    
    def test_create_user_admin(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        data = {
            "username": "andres",
            "password": "andres123",
            "document_manager": "1065840368",
            "names_manager": "Andres",
            "last_names_manager": "Martinez",
            "store_id": 1
        }
        response = self.client.post("/api/1.0/user-create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_auth_not_create_user(self):
        self.client.force_authenticate(user=None)
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        data = {
            "username": "andres",
            "password": "andres123",
            "document_manager": "1065840368",
            "names_manager": "Andres",
            "last_names_manager": "Martinez",
            "store_id": 1
        }
        response = self.client.post("/api/1.0/user-create/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
class CategoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin123", password="admin123", is_superuser=1)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
    
    def test_create_category(self):
        data = {
            "name" : "Pinturas",
            "description" : "Tipos de pintura"
        }
        response = self.client.post("/api/1.0/category-create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_auth_not_create_category(self):
        self.client.force_authenticate(user=None)
        data = {
            "name" : "Pinturas",
            "description" : "Tipos de pintura"
        }
        response = self.client.post("/api/1.0/category-create/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_category(self):

        data = {
            "name" : "Pinturas",
            "description" : "Tipos de pintura"
        }
        store = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        response = self.client.post("/api/1.0/category-edit/1", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_category(self):
        
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        category = Category.objects.create(name="Rodillos", description="Tipos de rodillos")
        response = self.client.get("/api/1.0/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_store(self):
        
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        response = self.client.get("/api/1.0/category-search/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class ProductTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="managerpintuco", password="managerpintuco123", is_superuser=0)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
    
    def test_create_product(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        data = {
            "category": 1,
            "name": "Pintura de aceite Plus extra",
            "price": 13000,
            "stock": 11
        }
        response = self.client.post("/api/1.0/product-create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_auth_not_create_product(self):
        self.client.force_authenticate(user=None)
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        data = {
            "category": 1,
            "name": "Pintura de aceite Plus extra",
            "price": 13000,
            "stock": 11
        }
        response = self.client.post("/api/1.0/product-create/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_edit_product(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus extra", price = 13000, stock=10)
        data = {
            "category": 1,
            "name": "Pintura de aceite Plus extra",
            "price": 15000,
            "stock": 11
        }
        response = self.client.post("/api/1.0/product-edit/1", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_product(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus maximun", price = 13000, stock=10)
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus ultra", price = 14000, stock=10)
        response = self.client.get("/api/1.0/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_product(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        response = self.client.get("/api/1.0/product-search/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_product(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        response = self.client.delete("/api/1.0/product-delete/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_not_delete_product_by_purchase(self):
        store = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_manager = StoreManager.objects.create(user = self.user,  store=store, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product = Product.objects.create(category=category, store=store, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        
        #make purchase with product
        client = Client.objects.create(names="Luis", last_names="Aponte", document="1065843703")
        purchase = Purchase.objects.create(client=client, value=36000)
        purchasedetail = PurchaseDetail.objects.create(purchase= purchase, product=product, stock_requested = 3, price_requested = 12000)
        response = self.client.delete("/api/1.0/product-delete/1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_catalog_product(self):
        self.client.force_authenticate(user=None)
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="245453453456-1")

        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")

        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 10000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus ultra", price = 12000, stock=10)
        product_3 = Product.objects.create(category=category, store=store_2, name="Pintura de aceite Plus ultra", price = 15000, stock=10)
        
        response = self.client.get("/api/1.0/catalog/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_catalog_product_by_store(self):
        self.client.force_authenticate(user=None)
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="245453453456-1")

        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")

        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 10000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus ultra", price = 12000, stock=10)
        product_3 = Product.objects.create(category=category, store=store_2, name="Pintura de aceite Plus ultra", price = 15000, stock=10)
        
        #with store_1
        response = self.client.get("/api/1.0/catalog-find/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PurchaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="managerpintuco", password="managerpintuco123", is_superuser=0)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)

    def test_create_purchase(self):
        self.client.force_authenticate(user=None)
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="346456456456-1")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")

        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_2, name="Alfombra roja", price = 13000, stock=10)
        
        #make purchase 
        data = {
                "client":{
                    "document" : "1244324323",
                    "names" : "Carlos",
                    "last_names" : "Perez"
                },
                "purchasedetail_set" : [
                    {
                        "stock_requested" : 4,
                        "product" : 1
                    },
                    {
                        "stock_requested" : 1,
                        "product" : 2
                    }
                ]
        }
        response = self.client.post("/api/1.0/purchase-create/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_purchase_with_errors_stock_product(self):
        self.client.force_authenticate(user=None)
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="346456456456-1")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")

        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 12000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_2, name="Alfombra roja", price = 13000, stock=10)
        
        #make purchase 
        data = {
                "client":{
                    "document" : "1244324323",
                    "names" : "Carlos",
                    "last_names" : "Perez"
                },
                "purchasedetail_set" : [
                    {
                        "stock_requested" : 4,
                        "product" : 1
                    },
                    {
                        "stock_requested" : 11,
                        "product" : 2
                    }
                ]
        }
        response = self.client.post("/api/1.0/purchase-create/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data[0]), "El producto con id 2 no cuenta con la cantidad solicitada.")

    def test_list_purchases_by_store_manager(self):
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="245453453456-1")
        #login with store_1
        store_manager = StoreManager.objects.create(user = self.user,  store=store_1, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 10000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus ultra", price = 12000, stock=10)
        product_3 = Product.objects.create(category=category, store=store_2, name="Pintura de aceite Plus ultra", price = 15000, stock=10)
        
        #make purchase with product
        client = Client.objects.create(names="Luis", last_names="Aponte", document="1065843703")
        purchase_1 = Purchase.objects.create(client=client, value=76000)
        purchase_2 = Purchase.objects.create(client=client, value=45000)

        purchasedetail_1 = PurchaseDetail.objects.create(purchase= purchase_1, product=product_1, stock_requested = 4, price_requested = 10000)
        purchasedetail_2 = PurchaseDetail.objects.create(purchase= purchase_1, product=product_2, stock_requested = 3, price_requested = 12000)
        purchasedetail_3 = PurchaseDetail.objects.create(purchase= purchase_2, product=product_3, stock_requested = 3, price_requested = 15000)
        
        response = self.client.get("/api/1.0/purchases")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_history_purchases_by_client(self):
        store_1 = Store.objects.create(name="Pintuco", document="2312341423344-1")
        store_2 = Store.objects.create(name="Comercar", document="245453453456-1")
        #login with store_1
        store_manager = StoreManager.objects.create(user = self.user,  store=store_1, document="1065777888", names="Juan", last_names="Perez")
        category = Category.objects.create(name="Pinturas", description="Tipos de pintura")
        product_1 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus extra", price = 10000, stock=10)
        product_2 = Product.objects.create(category=category, store=store_1, name="Pintura de aceite Plus ultra", price = 12000, stock=10)
        product_3 = Product.objects.create(category=category, store=store_2, name="Pintura de aceite Plus ultra", price = 15000, stock=10)
        
        #make purchase with product
        client = Client.objects.create(names="Luis", last_names="Aponte", document="1065843703")
        purchase_1 = Purchase.objects.create(client=client, value=76000)
        purchase_2 = Purchase.objects.create(client=client, value=45000)

        purchasedetail_1 = PurchaseDetail.objects.create(purchase= purchase_1, product=product_1, stock_requested = 4, price_requested = 10000)
        purchasedetail_2 = PurchaseDetail.objects.create(purchase= purchase_1, product=product_2, stock_requested = 3, price_requested = 12000)
        purchasedetail_3 = PurchaseDetail.objects.create(purchase= purchase_2, product=product_3, stock_requested = 2, price_requested = 15000)
        purchasedetail_4 = PurchaseDetail.objects.create(purchase= purchase_2, product=product_3, stock_requested = 1, price_requested = 15000)
        
        #with client
        response = self.client.get("/api/1.0/purchase-history-client/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
# Create your tests here.
