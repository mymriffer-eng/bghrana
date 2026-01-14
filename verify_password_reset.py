#!/usr/bin/env python
"""
Verify .env configuration and test password reset functionality
"""
import os
import sys

sys.path.insert(0, '/home/bghranac/repositories/bghrana')

print("=" * 70)
print("STEP 1: CHECK .ENV FILE")
print("=" * 70)

env_path = '/home/bghranac/repositories/bghrana/.env'
try:
    with open(env_path, 'r') as f:
        content = f.read()
    
    print("\nEmail-related settings in .env:")
    for line in content.split('\n'):
        if any(key in line for key in ['EMAIL_', 'DEFAULT_FROM_EMAIL']):
            print(f"  {line}")
except Exception as e:
    print(f"✗ Error reading .env: {e}")

print("\n" + "=" * 70)
print("STEP 2: LOAD DJANGO AND CHECK SETTINGS")
print("=" * 70)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')

try:
    import django
    django.setup()
    print("✓ Django loaded successfully")
    
    from django.conf import settings
    
    print(f"\nActive Django email settings:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
except Exception as e:
    print(f"✗ Error loading Django: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("STEP 3: TEST PASSWORD RESET FORM")
print("=" * 70)

try:
    from allauth.account.forms import ResetPasswordForm
    
    # Create form instance
    form = ResetPasswordForm(data={'email': 'test@example.com'})
    
    print("✓ ResetPasswordForm imported successfully")
    print(f"  Form fields: {list(form.fields.keys())}")
    
except Exception as e:
    print(f"✗ Error with ResetPasswordForm: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("STEP 4: TEST ACTUAL EMAIL SENDING")
print("=" * 70)

try:
    from django.core.mail import send_mail
    
    result = send_mail(
        'Password Reset Test - БГ Храна',
        'This is a test email for password reset functionality.',
        settings.DEFAULT_FROM_EMAIL,
        ['noreply@bghrana.com'],
        fail_silently=False,
    )
    
    print(f"✓ Test email sent successfully! (result: {result})")
    
except Exception as e:
    print(f"✗ Error sending test email: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("STEP 5: SIMULATE PASSWORD RESET REQUEST")
print("=" * 70)

try:
    from django.contrib.auth.models import User
    from allauth.account.models import EmailAddress
    
    # Check if we have any users
    user_count = User.objects.count()
    print(f"Total users in database: {user_count}")
    
    if user_count > 0:
        user = User.objects.first()
        print(f"Testing with user: {user.username} ({user.email})")
        
        # Try to trigger password reset
        from allauth.account.forms import ResetPasswordForm
        form = ResetPasswordForm(data={'email': user.email})
        
        if form.is_valid():
            form.save(request=None)
            print("✓ Password reset email would be sent!")
        else:
            print(f"✗ Form validation failed: {form.errors}")
    else:
        print("! No users in database to test with")
        
except Exception as e:
    print(f"✗ Error simulating password reset: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
