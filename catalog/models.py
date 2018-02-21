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




    # Product Types
    #     Category
    #         Name, Description, Create Date, Last Modified
    #     Bulk Product
    #         Name, Description, Category, Price, Create Date, Last Modified, Quantity, Reorder Trigger, Reorder Quantity
    #     Individual Product
    #         Name, Description, Category, Price, Create Date, Last Modified, Item ID
    #     Rental Product
    #         Name, Description, Category, Price, Create Date, Last Modified, Item ID, Max Rental, Retire Date
