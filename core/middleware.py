from ipware import get_client_ip

class CloudflareIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extracts the real IP from HTTP_CF_CONNECTING_IP or HTTP_X_FORWARDED_FOR
        client_ip, is_routable = get_client_ip(request)
        
        if client_ip:
            # Overrides Django's default IP variable so DRF rate limiting works correctly
            request.META['REMOTE_ADDR'] = client_ip
            
        return self.get_response(request)