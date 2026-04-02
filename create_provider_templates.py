#!/usr/bin/env python3
"""
ДИРЕКТНО СЪЗДАВАНЕ на provider-specific templates на production
"""
import os

print("=" * 70)
print("СЪЗДАВАНЕ НА PROVIDER TEMPLATES ДИРЕКТНО НА PRODUCTION")
print("=" * 70)

base_path = '/home/bghranac/public_html/catalog/templates/socialaccount'

# Facebook template
facebook_template = """{% extends 'socialaccount/base.html' %}
{% load static %}

{% block head_title %}Вход с Facebook{% endblock %}

{% block socialaccount_content %}
<div class="text-center mb-4">
  <div class="mb-3">
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48" fill="#1877F2">
      <path d="M24 4C12.955 4 4 12.955 4 24c0 9.99 7.325 18.273 16.875 19.742V29.344h-5.078V24h5.078v-4.078c0-5.014 2.987-7.781 7.554-7.781 2.188 0 4.476.39 4.476.39v4.922h-2.522c-2.484 0-3.258 1.543-3.258 3.125V24h5.547l-.887 5.344h-4.66v14.398C36.675 42.273 44 33.99 44 24c0-11.045-8.955-20-20-20z"/>
    </svg>
  </div>
  <p class="lead">Продължете като влезете с вашия Facebook акаунт</p>
</div>

<form method="post" class="d-grid">
  {% csrf_token %}
  <button type="submit" class="btn btn-primary btn-lg" style="background-color: #1877F2; border: none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-facebook me-2" viewBox="0 0 16 16">
      <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
    </svg>
    Продължи с Facebook
  </button>
</form>

<div class="text-center mt-4">
  <p class="text-muted small">
    Като натиснете "Продължи с Facebook", вие се съгласявате с нашите 
    <a href="{% url 'catalog:terms' %}" class="text-success">Общи условия</a> и 
    <a href="{% url 'catalog:cookie_policy' %}" class="text-success">Политика за бисквитки</a>
  </p>
</div>

<hr class="my-4">

<div class="text-center">
  <a href="{% url 'catalog:product_list' %}" class="btn btn-outline-secondary">
    ← Обратно към началната страница
  </a>
</div>
{% endblock %}
"""

# Google template
google_template = """{% extends 'socialaccount/base.html' %}
{% load static %}

{% block head_title %}Вход с Google{% endblock %}

{% block socialaccount_content %}
<div class="text-center mb-4">
  <div class="mb-3">
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
      <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
      <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
      <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
      <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
    </svg>
  </div>
  <p class="lead">Продължете като влезете с вашия Google акаунт</p>
</div>

<form method="post" class="d-grid">
  {% csrf_token %}
  <button type="submit" class="btn btn-success btn-lg" style="background-color: #0dd843; border: none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-google me-2" viewBox="0 0 16 16">
      <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z"/>
    </svg>
    Продължи с Google
  </button>
</form>

<div class="text-center mt-4">
  <p class="text-muted small">
    Като натиснете "Продължи с Google", вие се съгласявате с нашите 
    <a href="{% url 'catalog:terms' %}" class="text-success">Общи условия</a> и 
    <a href="{% url 'catalog:cookie_policy' %}" class="text-success">Политика за бисквитки</a>
  </p>
</div>

<hr class="my-4">

<div class="text-center">
  <a href="{% url 'catalog:product_list' %}" class="btn btn-outline-secondary">
    ← Обратно към началната страница
  </a>
</div>
{% endblock %}
"""

# Create directories
facebook_dir = os.path.join(base_path, 'facebook')
google_dir = os.path.join(base_path, 'google')

os.makedirs(facebook_dir, exist_ok=True)
os.makedirs(google_dir, exist_ok=True)

# Write Facebook template
facebook_file = os.path.join(facebook_dir, 'login.html')
with open(facebook_file, 'w', encoding='utf-8') as f:
    f.write(facebook_template)
print(f"✅ Създаден: {facebook_file}")
print(f"   Размер: {os.path.getsize(facebook_file)} bytes")

# Write Google template
google_file = os.path.join(google_dir, 'login.html')
with open(google_file, 'w', encoding='utf-8') as f:
    f.write(google_template)
print(f"✅ Създаден: {google_file}")
print(f"   Размер: {os.path.getsize(google_file)} bytes")

# Verify
print("\n" + "=" * 70)
print("ВЕРИФИКАЦИЯ:")
print("=" * 70)

for file in [facebook_file, google_file]:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Facebook' in content and file.endswith('facebook/login.html'):
                print(f"✅ {file} - съдържа 'Facebook'")
            elif 'Google' in content and file.endswith('google/login.html'):
                print(f"✅ {file} - съдържа 'Google'")
            else:
                print(f"⚠️  {file} - грешно съдържание")
    else:
        print(f"❌ {file} - НЕ СЪЩЕСТВУВА")

# Touch restart
import time
restart_file = '/home/bghranac/public_html/tmp/restart.txt'
os.makedirs(os.path.dirname(restart_file), exist_ok=True)
open(restart_file, 'a').close()
os.utime(restart_file, None)

print("\n✅ tmp/restart.txt updated за Passenger restart")

print("\n" + "=" * 70)
print("✅ ГОТОВО! Изчакай 10 секунди и тествай:")
print("   https://bghrana.com/accounts/facebook/login/")
print("   → ТРЯБВА да показва 'Вход с Facebook' (не Google)")
print("=" * 70)
