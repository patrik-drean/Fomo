from django.db import models

class Category(models.Model):
    Name = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    CreateDate = models.DateTimeField(null=True, blank=True)
    LastModified = models.DateTimeField(null=True, blank=True)

class Product(models.Model):
    Name = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    CreateDate = models.DateTimeField(null=True, blank=True)
    LastModified = models.DateTimeField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)

class BulkProduct(Product):
    Quantity = models.IntegerField(null=True, blank=True)
    ReorderTrigger = models.BooleanField( blank=True)
    ReorderQuantity = models.IntegerField(null=True, blank=True)

class IndividualProduct(Product):
    ItemID = models.IntegerField(null=True, blank=True)

class IndividualProduct(Product):
    ItemID = models.IntegerField(null=True, blank=True)
    MaxRental = models.IntegerField(null=True, blank=True)
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
