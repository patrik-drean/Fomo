from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
import datetime
import stripe
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#######################################################################
###   Products

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
        product = Product.objects.all().filter(id = id).first()
        urls = []
        if product is not None:
            for i in product.images.all():
                urls.append('/static/catalog/media/products/' + i.Filename)
        else:
            urls.append('/static/catalog/media/products/image_unavailable.gif')
        return urls

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

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


#######################################################################
###   Orders

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)


    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        # create a query object (filter to status='active')
        if include_tax_item:
            items = OrderItem.objects.filter(status='active', order_id = self.id )

        # if we aren't including the tax item, alter the
        # query to exclude that OrderItem
        # I simply used the product name (not a great choice,
        # but it is acceptable for credit)
        else:
            items = OrderItem.objects.filter(status='active',order_id = self.id).exclude(
                product_id = 75)

        return items




    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self,
                product=product,
                price=product.Price,
                quantity=0)
            print(item)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self, tax_included = False):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        # reset total Price
        self.total_price = 0

        # iterate the order items (not including tax item) and get the total price
        line_items = self.active_items()
        for line in line_items:
        # call recalculate on each item
            line.recalculate()
            if line.product.id == 75:
                tax_included = True
            else:
                self.total_price += line.extended

        # update/create the tax order item (calculate at 7% rate)
        tax_product = Product.objects.get(id = 75)
        if tax_included == False:
            tax_item = OrderItem()
            tax_item.product = tax_product
            tax_item.description = tax_product.Description
            self.get_item(product = tax_product, create=True)

        tax_line_item = self.get_item(tax_product)

        #activate tax if inactive
        tax_product.Status = 'A'
        tax_product.save()

        tax_line_item.price = Decimal(self.total_price) * Decimal(.07)
        tax_line_item.recalculate()
        tax_line_item.save()

        # update the total and save
        self.total_price += tax_line_item.price
        self.save()

    def finalize(self, stripe_charge_token, total_price):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():
            # recalculate just to be sure everything is updated
            self.recalculate()

            # check that all products are available

            for line_item in self.active_items():
                if line_item.product.Status != 'A':
                    # print('**************************')
                    # print(line_item.product.Status )
                    # print(line_item.product.Name )
                    raise ActiveException('Product unavailable')

            # contact stripe and run the payment (using the stripe_charge_token)

            charge  = stripe.Charge.create(
                currency = "usd",
                source = stripe_charge_token,
                amount = total_price,
                )

            # finalize (or create) one or more payment objects
            payment = Payment()
            payment.order = self
            payment.amount = total_price
            payment.validation_code = stripe_charge_token
            payment.save()

            # set order status to sold and save the order
            self.status = 'sold'
            self.save()

            # update product quantities for BulkProducts
            for line_item in self.active_items():
                if line_item.product.TITLE == 'BulkProduct':
                    line_item.product.Quantity -= line_item.quantity

                else:
                    line_item.product.Status = 'I'

                line_item.product.save()

            # send email receipt to customer
            fromaddr = "donotreply@musical-family.me"
            toaddr = self.user.email
            subject = 'Thank You for your Purchase!'#'FOMO Receipt'
            product_table = ''
            for line in self.active_items():
                product_table += """
                    <tr>
                      <td>""" + line.product.Name  +"""</td>
                      <td>""" + str(line.price) + """</td>
                      <td>
                """

                if line.product.id !=75:
                    product_table +=  str(line.quantity)

                product_table += """
                      </td>
                      <td>""" + str(line.extended) + """</td>
                    </tr>
                """

            message = """
                <h1> Order Confirmation: </h1>
                <p>Date: """ + datetime.date.today().strftime('%b %d, %Y') + """</p>
                <table class="table table-striped table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">Product</th>
                      <th scope="col">Price</th>
                      <th scope="col">Quantity</th>
                      <th scope="col">Extended</th>
                    </tr>
                  </thead>
                  <tbody>
                """ + product_table + """
                      <td></td>
                      <td></td>
                      <td><b>Total</b></td>
                      <td><b>Order Total: $""" + str(total_price/100) + """</b></td>
                  </tbody>
                </table>
                <style>
                    h1 {
                        
                    }
                    p, th, td {
                        font-size: 20px;
                    }
                </style>
            """

            # 2.	When the finalize() method is called (upon finalization of a sale),
            # email a receipt to the user.  This can be the same (or nearly the same)
            # template you use for the browser-based receipt page.
            # It should show the sale information, including the date, total,
            # sale items, tax, shipping, etc.

            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject

            body = message
            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP('mail.musical-family.me', 25)
            # server.starttls()
            # server.login(fromaddr, "TestAcount")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            # server.quit()




class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.Name, self.extended)


    def recalculate(self):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        if self.price is None or self.price == 0:
            self.price = self.product.Price

        # default the quantity to 1 if we don't have a quantity set
        if self.quantity == 0:
            self.quantity = 1


        # calculate the extended (price * quantity)
        self.extended = self.price * self.quantity

        # save the changes
        self.save()


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)

class ActiveException(Exception):
    pass
