"""
Custom security middleware for additional protection
"""
import re
from django.http import HttpResponseForbidden
from django.conf import settings
from ipaddress import ip_network, ip_address


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
        response['Referrer-Policy'] = 'no-referrer-when-downgrade'
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


class AdminRestrictMiddleware:
    """
    Restrict access to Django admin based on IPs listed in .env as ADMIN_ALLOWED_IPS.
    Format: comma-separated IPs or CIDRs, e.g. "127.0.0.1, 192.168.0.0/24".
    Returns 403 Forbidden if client IP is not allowed.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Adjust if your admin path differs (we use /secure-panel/ in this project)
        self.admin_path = '/secure-panel/'
        raw = getattr(settings, 'ADMIN_ALLOWED_IPS', '') or ''
        self.networks = []
        for part in [p.strip() for p in raw.split(',') if p.strip()]:
            try:
                network = ip_network(part, strict=False)
            except ValueError:
                network = ip_network(part + '/32', strict=False)
            self.networks.append(network)

    def __call__(self, request):
        if request.path.startswith(self.admin_path):
            client_ip = (request.META.get('HTTP_X_FORWARDED_FOR', '') or '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', '')
            if self.networks:
                try:
                    addr = ip_address(client_ip)
                    if not any(addr in net for net in self.networks):
                        return HttpResponseForbidden('Admin access restricted')
                except ValueError:
                    return HttpResponseForbidden('Admin access restricted')
        return self.get_response(request)

