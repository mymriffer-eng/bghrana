"""
Security Headers Middleware
Добавя допълнителни security headers към всички HTTP отговори
"""

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content-Security-Policy - защита от XSS атаки
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://accounts.google.com https://apis.google.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "img-src 'self' data: https: blob:; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
            "connect-src 'self' https://accounts.google.com; "
            "frame-src https://accounts.google.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self' https://accounts.google.com; "
            "upgrade-insecure-requests;"
        )
        
        # Permissions-Policy - контрол на браузърни функции
        response['Permissions-Policy'] = (
            "geolocation=(), "
            "camera=(), "
            "microphone=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        )
        
        # Cross-Origin-Embedder-Policy
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        
        # Cross-Origin-Resource-Policy
        response['Cross-Origin-Resource-Policy'] = 'same-origin'
        
        # Премахване на X-Powered-By header (ако съществува)
        if 'X-Powered-By' in response:
            del response['X-Powered-By']
        
        return response
