from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Category, Product, Purchase, PurchaseDetail, Store, StoreManager
from django.contrib.auth.models import User
from .serializers import UserSerializer, CategorySerializer, StoreSerializer, ProductSerializer, PurchaseSerializer, PurchaseSearchSerializer

#views USER
@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def userCreate(request):
    error = True
    message = ""
    http_status = status.HTTP_400_BAD_REQUEST

    user = request.user
    user_permission = User.objects.filter(username = user).filter(is_superuser = 1)
    if len(user_permission) > 0:
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            http_status = status.HTTP_201_CREATED
            error = False
            message = "Usuario registrado exitosamente."
        else:
            message = serializer.errors
            http_status = status.HTTP_400_BAD_REQUEST
    else:
        message = "No tiene acceso para realizar esta acción"
        http_status = status.HTTP_401_UNAUTHORIZED

    response = {'error' : error, 'message' : message}
    return Response(response, http_status)


#views CATEGORY
@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def categoryList(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def categorySearch(request, pk):
    category = Category.objects.get(id=pk)
    serializer = CategorySerializer(category, many = False)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def categoryCreate(request):
    user = request.user
    user_permission = User.objects.filter(username = user).filter(is_superuser = 1)
    if len(user_permission) > 0:
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene acceso para realizar esta acción", status = status.HTTP_401_UNAUTHORIZED)


@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def categoryEdit(request, pk):
    user = request.user
    user_permission = User.objects.filter(username = user).filter(is_superuser = 1)
    if len(user_permission) > 0:
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(instance = category ,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            response = {'error' : True, 'message' : 'Categoria no existe.'}
            return Response(response, status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response("No tiene acceso para realizar esta acción", status = status.HTTP_401_UNAUTHORIZED)
    

#views STORE

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def storeList(request):
    shops = Store.objects.all()
    serializer = StoreSerializer(shops, many = True)
    data = {
        'shops' : serializer.data
    }
    return Response(data, status = status.HTTP_200_OK)

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def storeSearch(request, pk):
    store = Store.objects.get(id=pk)
    serializer = StoreSerializer(store, many = False)
    data = {
        'shops' : serializer.data
    }
    return Response(data, status = status.HTTP_200_OK)

@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def storeCreate(request):
    user = request.user
    user_permission = User.objects.filter(username = user).filter(is_superuser = 1)
    if len(user_permission) > 0:
        serializer = StoreSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response("No tiene acceso para realizar esta acción", status = status.HTTP_401_UNAUTHORIZED)


@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def storeEdit(request, pk):
    user = request.user
    user_permission = User.objects.filter(username = user).filter(is_superuser = 1)
    if len(user_permission) > 0:
        try:
            store = Store.objects.get(id=pk)
            serializer = StoreSerializer(instance = store ,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist:
            response = {'error' : True, 'message' : 'Tienda no existe.'}
            return Response(response, status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response("No tiene acceso para realizar esta acción", status = status.HTTP_401_UNAUTHORIZED)
    

#views PRODUCT

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def productList(request):
    user =  request.user
    if user.is_superuser == 1:
        products = Product.objects.all()
    else:
        store_manager = StoreManager.objects.get(user_id = user.id)
        products = Product.objects.filter(store_id = store_manager.store_id)

    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def productSearch(request, pk):
    manager_permission = StoreManager.objects.filter(user__username = request.user.username)
    if len(manager_permission) > 0:
        #set store according to user
        store_id =  manager_permission[0].store_id
        
        try:
            product = Product.objects.get(id=pk)
            if product.store_id != store_id: 
                response = {'error' : True, 'message' : 'Producto no existe.'}
                return Response(response, status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            response = {'error' : True, 'message' : 'Producto no existe.'}
            return Response(response, status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(product, many = False)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def productCreate(request):
    error = True
    message = ""
    http_status = ""
    manager_permission = StoreManager.objects.filter(user__username = request.user.username)
    if len(manager_permission) > 0:

        #set store according to user
        request.data._mutable = True
        request.data['store'] = manager_permission[0].store_id
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            error = False
            http_status = status.HTTP_201_CREATED
            message = "Producto registrado exitosamente."
        else:
            http_status = status.HTTP_400_BAD_REQUEST
            message = serializer.errors
    else:
        http_status = status.HTTP_401_UNAUTHORIZED
        message = "No tiene acceso para realizar esta acción"

    response = {'error' : error, 'message' : message}
    return Response(response, http_status)

@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def productEdit(request, pk):
    error = True
    message = ""
    http_status = ""
    manager_permission = StoreManager.objects.filter(user__username = request.user.username)
    if len(manager_permission) > 0:

        #set store according to user
        request.data._mutable = True
        request.data['store'] = manager_permission[0].store_id
        
        try:
            product = Product.objects.get(id=pk)
            if product.store_id != manager_permission[0].store_id: 
                response = {'error' : True, 'message' : 'Producto no existe.'}
                return Response(response, status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            response = {'error' : True, 'message' : 'Producto no existe.'}
            return Response(response, status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(instance = product ,data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            error = False
            http_status = status.HTTP_201_CREATED
            message = "Producto editado exitosamente."
        else:
            http_status = status.HTTP_400_BAD_REQUEST
            message = serializer.errors
    else:
        http_status = status.HTTP_401_UNAUTHORIZED
        message = "No tiene acceso para realizar esta acción"

    response = {'error' : error, 'message' : message}
    return Response(response, http_status)
   

@api_view(('DELETE',))
@permission_classes((IsAuthenticated,))
def productDelete(request, pk):
    error = True
    message = ""
    http_status = ""
    manager_permission = StoreManager.objects.filter(user__username = request.user.username)
    if len(manager_permission) > 0:

        try:
            product = Product.objects.get(id=pk)
            if product.store_id != manager_permission[0].store_id: 
                response = {'error' : True, 'message' : 'Producto no existe.'}
                return Response(response, status.HTTP_400_BAD_REQUEST)
            
            #validate purchases
            purchases = PurchaseDetail.objects.filter(product_id = product.id)
            if len(purchases) == 0:
                product.delete()
                error = False
                message = "Producto eliminado exitosamente."
                http_status = status.HTTP_200_OK
            else:
                message = "No puede realizar la eliminacion debido a que el producto tiene compras asociadas."
                http_status = status.HTTP_400_BAD_REQUEST
        except Product.DoesNotExist:
            response = {'error' : True, 'message' : 'Producto no existe.'}
            return Response(response, status.HTTP_400_BAD_REQUEST)
        
    else:
        http_status = status.HTTP_401_UNAUTHORIZED
        message = "No tiene acceso para realizar esta acción"

    response = {'error' : error, 'message' : message}
    return Response(response, http_status)


#views PURCHASE
@api_view(('POST',))
def purchaseCreate(request): 
    error = True
    message = ""
    http_status = ""
    serializer = PurchaseSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        error = False
        http_status = status.HTTP_201_CREATED
        message = "Compra registrada exitosamente." 
    else:
        http_status = status.HTTP_400_BAD_REQUEST
        message = serializer.errors

    response = {'error' : error, 'message' : message}
    return Response(response, http_status)


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def purchaseList(request):
    user =  request.user
    if user.is_superuser == 1:
        purchases = Purchase.objects.all()
    else:
        store_manager = StoreManager.objects.get(user_id = user.id)
        purchases = Purchase.objects.filter(purchasedetail__product__store_id = store_manager.store_id)
    serializer = PurchaseSearchSerializer(purchases, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('GET',))
def productCatalog(request):
    products = Product.objects.filter(stock__gt = 0)
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('GET',))
def productCatalogFindStore(request, pk):
     products = Product.objects.filter(stock__gt = 0).filter(store_id=pk)
     serializer = ProductSerializer(products, many = True)
     return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(('GET',))
def purchaseHistoryClient(request, pk):
    purchases = Purchase.objects.filter(client_id = pk)
    serializer = PurchaseSearchSerializer(purchases, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)