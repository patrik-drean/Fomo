from catalog import models as cmod

class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_five = []
        # One-time configuration and initialization.

    def __call__(self, request):

        productids = request.session.get('productids')
        products = []

        if productids is not None:
            for pid in productids:
                products.append(cmod.Product.objects.get(id = pid))

        self.last_five = products

        request.last_five = self.last_five






        response = self.get_response(request)






        productids = []
        for p in products:
            productids.append(int(p.id))

        request.session['productids'] = productids
        self.last_five = productids


        return response

# Before the request
#     request.session -> dictionary
#     product_ids = session.get ids from the sessions
#     products = [list of id's to actual objects]
#     request.last_five = [product objects]


# After the request
#     convert request.last_five -> list of ids
#     set list of ids into session
