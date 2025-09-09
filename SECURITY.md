# Security Guide for Django Personal Site

## Security Checklist

### ✅ Implemented Security Measures

1. **Environment Variables**
   - Moved sensitive settings to environment variables
   - Created `.env` file for configuration
   - Using `python-decouple` for secure configuration management

2. **Security Headers**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin
   - Content Security Policy (CSP)
   - Permissions Policy

3. **HTTPS Configuration**
   - SECURE_SSL_REDIRECT (set to True in production)
   - SESSION_COOKIE_SECURE (set to True in production)
   - CSRF_COOKIE_SECURE (set to True in production)
   - HSTS headers configured

4. **Session Security**
   - Session timeout: 1 hour
   - HttpOnly cookies enabled
   - Secure cookies (in production)
   - Session expiration at browser close

5. **CSRF Protection**
   - CSRF middleware enabled
   - HttpOnly CSRF cookies
   - CSRF tokens in forms

6. **Password Security**
   - Minimum length: 8 characters
   - Password validation enabled
   - User attribute similarity check
   - Common password check
   - Numeric password check

7. **Rate Limiting**
   - Custom rate limiting middleware
   - 1000 requests per hour per IP
   - Automatic cleanup of old entries

8. **Bot Protection**
   - User agent filtering
   - Blocks common security scanners
   - Blocks suspicious crawlers

9. **Logging**
   - Comprehensive logging configuration
   - Security event logging
   - File and console logging

10. **Static Files**
    - WhiteNoise for secure static file serving
    - Compressed and cached static files

## Production Deployment Security

### 1. Environment Setup

Create a `.env` file with production values:

```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Production settings
SECRET_KEY=''
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Database Security

For production, consider using PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

### 3. Web Server Configuration

#### Nginx Configuration Example:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. SSL/TLS Configuration

- Use Let's Encrypt for free SSL certificates
- Configure automatic renewal
- Use strong cipher suites
- Enable HSTS

### 5. Firewall Configuration

```bash
# UFW firewall rules
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 6. Regular Security Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
pip install --upgrade -r requirements.txt

# Update Django
pip install --upgrade Django
```

## Security Monitoring

### 1. Log Monitoring

Monitor these log files:
- `/var/log/nginx/access.log`
- `/var/log/nginx/error.log`
- `logs/django.log`
- `/var/log/auth.log`

### 2. Security Tools

Consider implementing:
- Fail2ban for brute force protection
- ModSecurity WAF
- Regular security scans
- Backup monitoring

### 3. Backup Strategy

```bash
# Database backup
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# File backup
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz media/ staticfiles/
```

## Additional Security Recommendations

1. **Regular Security Audits**
   - Run `python manage.py check --deploy`
   - Use security scanning tools
   - Monitor for vulnerabilities

2. **Access Control**
   - Use strong admin passwords
   - Enable two-factor authentication
   - Limit admin access to specific IPs

3. **Data Protection**
   - Encrypt sensitive data
   - Regular data backups
   - GDPR compliance (if applicable)

4. **Monitoring**
   - Set up alerts for security events
   - Monitor for unusual traffic patterns
   - Regular log analysis

## Emergency Response

### If Compromised:

1. **Immediate Actions**
   - Take site offline
   - Change all passwords
   - Review logs for intrusion points
   - Restore from clean backup

2. **Investigation**
   - Analyze attack vectors
   - Identify vulnerabilities
   - Document incident

3. **Recovery**
   - Patch vulnerabilities
   - Implement additional security measures
   - Restore service

## Security Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)


