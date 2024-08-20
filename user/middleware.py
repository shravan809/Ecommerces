import time
from django.core.cache import cache
from django.http import HttpResponseBadRequest

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 3  # Limit to 100 requests
        self.time_window = 60  # In a 60-second window

    def __call__(self, request):
        # Identify the user by IP address or authentication token
        user_id = request.META.get('REMOTE_ADDR')

        # Check the number of requests in the time window
        request_count = cache.get(user_id, 0)

        if request_count >= self.rate_limit:
            
            return HttpResponseBadRequest("Too many requests. Please try again later.")

        # Increment the request count and set it with an expiry time
        cache.set(user_id, request_count + 1, timeout=self.time_window)

        # Proceed with the request
        response = self.get_response(request)
        return response
