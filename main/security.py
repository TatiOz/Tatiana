"""
Custom security middleware for additional protection
"""
import re
from django.http import HttpResponseForbidden
from django.conf import settings


class SecurityMiddleware:
    """
    Custom security middleware to add additional security headers
    and protect against common attacks
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        return response
    
    def process_request(self, request):
        # Block suspicious user agents
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        suspicious_patterns = [
            r'bot',
            r'crawler',
            r'spider',
            r'scanner',
            r'nmap',
            r'sqlmap',
            r'nikto',
            r'w3af',
            r'burp',
            r'zap',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                return HttpResponseForbidden("Access denied")
        
        return None


class RateLimitMiddleware:
    """
    Simple rate limiting middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
        
    def __call__(self, request):
        # Simple IP-based rate limiting
        client_ip = self.get_client_ip(request)
        
        # Clean old entries (older than 1 hour)
        current_time = time.time()
        self.request_counts = {
            ip: count for ip, count in self.request_counts.items()
            if current_time - count['timestamp'] < 3600
        }
        
        # Check rate limit
        if client_ip in self.request_counts:
            if self.request_counts[client_ip]['count'] > 1000:  # 1000 requests per hour
                return HttpResponseForbidden("Rate limit exceeded")
            self.request_counts[client_ip]['count'] += 1
        else:
            self.request_counts[client_ip] = {
                'count': 1,
                'timestamp': current_time
            }
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


import time
