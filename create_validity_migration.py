#!/usr/bin/env python3
"""
Create migration and apply it - for validity_period field
Run from cPanel: Run Python Script
"""
import os
import subprocess

print("=" * 60)
print("CREATE & APPLY MIGRATION FOR VALIDITY_PERIOD")
print("=" * 60)

os.chdir('/home/bghranac/public_html')

print("\n1. Making migrations...")
print("-" * 60)
result = subprocess.run(['python', 'manage.py', 'makemigrations', 'catalog'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

if result.returncode != 0:
    print("\n❌ FAILED to create migration!")
    exit(1)

print("\n2. Applying migrations...")
print("-" * 60)
result = subprocess.run(['python', 'manage.py', 'migrate'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

if result.returncode != 0:
    print("\n❌ FAILED to apply migration!")
    exit(1)

print("\n3. Restarting Passenger...")
print("-" * 60)
restart_file = '/home/bghranac/public_html/tmp/restart.txt'
os.makedirs(os.path.dirname(restart_file), exist_ok=True)
with open(restart_file, 'w') as f:
    f.write('restart')
print("✅ Restart file created")

print("\n" + "=" * 60)
print("✅ SUCCESS! SITE SHOULD WORK IN 30-60 SECONDS")
print("=" * 60)
