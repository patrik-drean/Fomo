class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

# Before the request
#     request.session -> dictionary
#     product_ids = session.get ids from the sessions
#     products = [list of id's to actual objects]
#     request.last_five = [product objects]


# After the request
#     convert request.last_five -> list of ids
#     set list of ids into session
