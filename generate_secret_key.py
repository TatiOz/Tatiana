#!/usr/bin/env python3
"""
Script to generate a secure Django secret key
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("Generated Django Secret Key:")
    print(secret_key)
    print("\nAdd this to your .env file:")
    print(f"SECRET_KEY={secret_key}")


