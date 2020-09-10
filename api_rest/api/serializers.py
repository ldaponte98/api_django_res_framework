from rest_framework import serializers
from django.utils import timezone
from .models import Client, Category, Product, Purchase, PurchaseDetail, Store, StoreManager
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'document',
            'names',
            'last_names',
        )
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
        )

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'document'
        )

class StoreProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'document'
        )
class ProductSearchSerializer(serializers.ModelSerializer):
    store = StoreSerializer(many=False)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
            'category',
            'store',
        )
class ProductSerializer(serializers.ModelSerializer):
    #store = StoreSerializer(many=False)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
            'category',
            'store',
        )

class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    password = serializers.CharField()
    document_manager = serializers.CharField()
    names_manager = serializers.CharField()
    last_names_manager = serializers.CharField()
    store_id = serializers.IntegerField()


    def create(self, validate_data):
        instance = User()
        instance.username = validate_data.get('username')
        instance.is_superuser = 0
        instance.set_password(validate_data.get('password'))
        instance.save()

        store_manager = StoreManager()
        store_manager.document = validate_data.get('document_manager')
        store_manager.names = validate_data.get('names_manager')
        store_manager.last_names = validate_data.get('last_names_manager')
        store_manager.store_id = validate_data.get('store_id')
        store_manager.user_id = instance.id
        store_manager.save()

        return instance

    def validate_store_id(self, data):
        shops = Store.objects.filter(id = data)
        if len(shops) == 0:
            raise serializers.ValidationError("Esta tienda no existe.")
        else:
            return data
    
    def validate_username(self, data):
        users = User.objects.filter(username = data)
        if len(users) > 0:
            raise serializers.ValidationError("Este nombre de usuario ya existe.")
        else:
            return data

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','document', 'names', 'last_names']


class PurchaseDetailSearchSerializer(serializers.ModelSerializer):
    product = ProductSearchSerializer(many=False)
    class Meta:
        model = PurchaseDetail
        fields = ['id','product', 'stock_requested']


class PurchaseSearchSerializer(serializers.ModelSerializer):
    purchasedetail_set = PurchaseDetailSearchSerializer(many=True)
    client = ClientSerializer(many=False)
    class Meta:
        model = Purchase
        fields = ['id','value','date','client', 'purchasedetail_set']

class PurchaseDetailSerializer(serializers.ModelSerializer):
    #product = ProductSerializer(many=False)
    class Meta:
        model = PurchaseDetail
        fields = ['id','product', 'stock_requested']

class PurchaseSerializer(serializers.ModelSerializer):
    purchasedetail_set = PurchaseDetailSerializer(many=True)
    client = ClientSerializer(many=False)
    class Meta:
        model = Purchase
        fields = ['id','date','client', 'purchasedetail_set']


    def create(self, validated_data):

        purchasedetails = validated_data.pop('purchasedetail_set')
        
        if self.validate_stock_product(purchasedetails) == True:
            data_client = validated_data.get('client')
            client = Client.objects.filter(document=data_client['document'])
            if len(client) == 0:
                client =  Client.objects.create(names=data_client['names'], last_names=data_client['last_names'], document=data_client['document'])
            else:
                client = client[0]
            purchase = Purchase.objects.create(client=client,value=0)
            value = 0
            for detail in purchasedetails:
                purchase_detail = PurchaseDetail()
                purchase_detail.purchase = purchase
                purchase_detail.product_id = detail['product'].id
                purchase_detail.price_requested = detail['product'].price
                purchase_detail.stock_requested = detail['stock_requested']
                purchase_detail.save()
                product = Product.objects.get(id = detail['product'].id)
                product.discount(detail['stock_requested'])
                value += detail['product'].price * purchase_detail.stock_requested
            
            purchase.value = value
            purchase.save()
            return purchase

    def validate_stock_product(self, purchasedetails):
            
            for detail in purchasedetails:
                
                try:
                    product = Product.objects.get(id=detail['product'].id)
                    
                    if (product.stock - detail['stock_requested']) < 0 :
                        raise serializers.ValidationError("El producto con id "+str(detail['product'].id)+" no cuenta con la cantidad solicitada.")
                        return False
                except Product.DoesNotExist:
                    raise serializers.ValidationError("El producto con id "+str(detail['product'].id)+" no es valido.")
                    return False
            return True

    
