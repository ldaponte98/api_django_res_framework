from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Client(models.Model):
    id = models.AutoField(primary_key = True)
    document = models.CharField('Identificacion', max_length = 25)    
    names = models.CharField('Nombres', max_length = 100)    
    last_names = models.CharField('Apellidos', max_length = 150)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1},{2}'.format(self.document, self.names, self.last_names)


class Category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 100)    
    description = models.CharField('Descripcion', max_length = 300)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1}'.format(self.name, self.description)

class Store(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 100)    
    document = models.CharField('Nit', max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1}'.format(self.name, self.document)

class Product(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 100)    
    price = models.DecimalField(max_digits=15, decimal_places=0)
    stock = models.DecimalField(max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1}'.format(self.name)
    
    def discount(self, stock):
        self.stock -= stock 
        self.save()


class Purchase(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateTimeField(auto_now_add=True)    
    value = models.DecimalField(max_digits=30, decimal_places=0)
    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1}'.format(self.date, self.value)

class PurchaseDetail(models.Model):
    id = models.AutoField(primary_key = True)
    purchase = models.ForeignKey(Purchase, on_delete = models.CASCADE)  
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    stock_requested = models.DecimalField(max_digits=30, decimal_places=0)
    price_requested = models.DecimalField(max_digits=30, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1}.{2}'.format(self.product.id, self.stock, self.price_product)

class StoreManager(models.Model):
    id = models.AutoField(primary_key = True)
    document = models.CharField('Identificacion', max_length = 25)    
    names = models.CharField('Nombres', max_length = 100)    
    last_names = models.CharField('Apellidos', max_length = 150)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{0},{1},{2}'.format(self.document, self.names, self.last_names)