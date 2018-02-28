from django.db import models
from polymorphic.models import PolymorphicModel

class Category(models.Model):
    Name = models.TextField()
    Description = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

# products[0].__class__.__name__ = 'BulkProdcut'
# pip3 install django-polymorphic
class Product(PolymorphicModel):
    TYPE_CHOICES = (
    ('BulkProduct', 'Bulk Product'),
    ('IndividualProduct', 'Individual Product'),
    ('RentalProduct', 'Rental Product'),
    )

    STATUS_CHOICES = (
    ('A', 'Active'),
    ('I', 'Inactive'),
    )

    Name = models.TextField()
    Description = models.TextField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=8, decimal_places=2)
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)
    Status = models.TextField(choices=STATUS_CHOICES, default='A')

    def new_object(self, name = '', description = '', category = None, price = 0, status = 'A'):
        self.Name = name
        self.Description = description
        self.Category = category
        self.Price = price
        self.Status = status

    # convenience method
    def image_url(self, id):
        ''' Always return an image '''
        product = ProductImage.objects.all().filter(Product_id = id).first()
        if product is not None:
            url = '/static/catalog/media/products/' + product.Filename
        else:
            url = '/static/catalog/media/products/image_unavailable.gif'
        return url

    def image_urls(self, id):
        '''Returns a list of all images for that product'''
        product = ProductImage.objects.all().filter(Product_id = id)
        urls = []
        if product is not None:
            for i in product.images:
                urls.append('/static/catalog/media/products/' + i.Filename)
        else:
            urls.append('/static/catalog/media/products/image_unavailable.gif')
        return urls

class BulkProduct(Product):
    TITLE = 'BulkProduct'
    Quantity = models.IntegerField()
    ReorderTrigger = models.IntegerField()
    ReorderQuantity = models.IntegerField()

class IndividualProduct(Product):
    TITLE = 'IndividualProduct'
    ItemID = models.TextField()

class RentalProduct(Product):
    TITLE = 'RentalProduct'
    ItemID = models.TextField()
    MaxRental = models.IntegerField()
    RetireDate = models.DateTimeField(null=True, blank=True)

class ProductImage(models.Model):
    Filename = models.TextField()
    Product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)
