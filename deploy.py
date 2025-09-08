#!/usr/bin/env python3
"""
Deployment script for secure Django site
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    requirements = [
        'django',
        'python-decouple',
        'whitenoise',
        'gunicorn',
        'django-cors-headers',
        'django-ratelimit',
        'django-axes',
    ]
    
    for req in requirements:
        try:
            __import__(req.replace('-', '_'))
            print(f"✅ {req}")
        except ImportError:
            print(f"❌ {req} - Missing")
            return False
    return True

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_migrations():
    """Run database migrations"""
    return run_command("python manage.py migrate", "Running migrations")

def check_security():
    """Run security checks"""
    return run_command("python manage.py check --deploy", "Running security checks")

def create_superuser():
    """Create superuser if needed"""
    print("👤 Do you want to create a superuser? (y/n): ", end="")
    response = input().lower()
    if response == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")

def main():
    """Main deployment function"""
    print("🚀 Django Site Deployment Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Some requirements are missing. Please install them first.")
        sys.exit(1)
    
    # Run security checks
    if not check_security():
        print("❌ Security checks failed. Please fix issues before deployment.")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Database migrations failed.")
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        print("❌ Static file collection failed.")
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    print("\n✅ Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your web server (Nginx/Apache)")
    print("2. Set up SSL certificates")
    print("3. Configure environment variables")
    print("4. Set up monitoring and logging")
    print("5. Test the deployment")

if __name__ == "__main__":
    main()
