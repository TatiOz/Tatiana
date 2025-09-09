#!/usr/bin/env python3
"""
Security check script for Django site
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_site.settings')
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line

def check_security_settings():
    """Check security-related settings"""
    print("🔒 Security Configuration Check")
    print("=" * 50)
    
    # Check DEBUG setting
    if settings.DEBUG:
        print("⚠️  WARNING: DEBUG is set to True")
        print("   Set DEBUG=False in production")
    else:
        print("✅ DEBUG is set to False")
    
    # Check SECRET_KEY
    if 'django-insecure' in settings.SECRET_KEY:
        print("⚠️  WARNING: Using default Django secret key")
        print("   Generate a new secret key for production")
    else:
        print("✅ Custom secret key is configured")
    
    # Check ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS:
        print("⚠️  WARNING: ALLOWED_HOSTS is empty")
        print("   Configure ALLOWED_HOSTS for production")
    else:
        print(f"✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}")
    
    # Check HTTPS settings
    if not settings.SECURE_SSL_REDIRECT:
        print("⚠️  WARNING: SECURE_SSL_REDIRECT is False")
        print("   Set to True in production with HTTPS")
    else:
        print("✅ SECURE_SSL_REDIRECT is enabled")
    
    if not settings.SESSION_COOKIE_SECURE:
        print("⚠️  WARNING: SESSION_COOKIE_SECURE is False")
        print("   Set to True in production")
    else:
        print("✅ SESSION_COOKIE_SECURE is enabled")
    
    if not settings.CSRF_COOKIE_SECURE:
        print("⚠️  WARNING: CSRF_COOKIE_SECURE is False")
        print("   Set to True in production")
    else:
        print("✅ CSRF_COOKIE_SECURE is enabled")
    
    # Check security headers
    print("\n🔒 Security Headers:")
    print(f"   X_FRAME_OPTIONS: {settings.X_FRAME_OPTIONS}")
    print(f"   SECURE_BROWSER_XSS_FILTER: {settings.SECURE_BROWSER_XSS_FILTER}")
    print(f"   SECURE_CONTENT_TYPE_NOSNIFF: {settings.SECURE_CONTENT_TYPE_NOSNIFF}")
    print(f"   SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")
    
    # Check middleware
    print("\n🛡️  Security Middleware:")
    security_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'main.security.SecurityMiddleware',
        'main.security.RateLimitMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ]
    
    for middleware in security_middleware:
        if middleware in settings.MIDDLEWARE:
            print(f"   ✅ {middleware}")
        else:
            print(f"   ❌ {middleware} - Missing")
    
    # Check password validators
    print(f"\n🔐 Password Validators: {len(settings.AUTH_PASSWORD_VALIDATORS)} configured")
    
    # Check logging
    if hasattr(settings, 'LOGGING') and settings.LOGGING:
        print("✅ Logging is configured")
    else:
        print("⚠️  WARNING: Logging is not configured")

def run_django_check():
    """Run Django's built-in security check"""
    print("\n🔍 Running Django Security Check")
    print("=" * 50)
    
    try:
        # Run Django's check command
        execute_from_command_line(['manage.py', 'check', '--deploy'])
    except SystemExit as e:
        if e.code == 0:
            print("✅ Django security check passed")
        else:
            print("❌ Django security check failed")

if __name__ == "__main__":
    check_security_settings()
    run_django_check()
    
    print("\n📋 Next Steps:")
    print("1. Create a .env file with production settings")
    print("2. Generate a new secret key")
    print("3. Configure HTTPS in production")
    print("4. Set up proper logging and monitoring")
    print("5. Regular security updates")


