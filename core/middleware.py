from django.http import HttpResponseForbidden
from django.conf import settings


class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in settings.ALLOWED_IPS:
            return HttpResponseForbidden('Acesso negado.')
        return self.get_response(request)