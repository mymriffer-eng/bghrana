#!/usr/bin/env python
"""
Показва ТОЧНОТО съдържание на Facebook template
+ проверява дали наследява правилно base template
"""

import os

print("=" * 70)
print("FACEBOOK TEMPLATE CONTENT INSPECTION")
print("=" * 70)

fb_template = '/home/bghranac/public_html/catalog/templates/socialaccount/facebook/login.html'

print(f"\n📄 FILE: {fb_template}")
print(f"   Exists: {os.path.exists(fb_template)}")
print(f"   Size: {os.path.getsize(fb_template)} bytes")

print("\n" + "=" * 70)
print("FULL CONTENT:")
print("=" * 70)

with open(fb_template, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

print("\n" + "=" * 70)
print("ANALYSIS:")
print("=" * 70)

# Проверка на extends
if '{% extends' in content:
    import re
    match = re.search(r'{%\s*extends\s+["\']([^"\']+)["\']', content)
    if match:
        parent = match.group(1)
        print(f"✅ Extends: {parent}")
        
        # Проверка дали parent template съществува
        if parent.startswith('socialaccount/'):
            parent_path = f'/home/bghranac/public_html/catalog/templates/{parent}'
            if os.path.exists(parent_path):
                print(f"   ✅ Parent exists: {parent_path}")
                
                # Четем parent template
                with open(parent_path, 'r', encoding='utf-8') as pf:
                    parent_content = pf.read(300)
                    if 'Google' in parent_content:
                        print(f"   ⚠️ PARENT CONTAINS 'Google'!")
                        print(f"      Това може да е проблемът!")
            else:
                print(f"   ❌ Parent NOT FOUND: {parent_path}")
else:
    print("⚠️ NO {% extends %} found!")

# Проверка на blocks
import re
blocks = re.findall(r'{%\s*block\s+(\w+)\s*%}', content)
if blocks:
    print(f"\n✅ Blocks defined: {blocks}")
else:
    print("\n⚠️ NO blocks defined!")

# Проверка за Facebook text
if 'Facebook' in content:
    print("\n✅ Contains 'Facebook'")
    facebook_count = content.count('Facebook')
    print(f"   Occurrences: {facebook_count}")
else:
    print("\n❌ DOES NOT contain 'Facebook'!")

if 'Google' in content:
    print("\n❌ WARNING: Contains 'Google'!")
    google_count = content.count('Google')
    print(f"   Occurrences: {google_count}")

print("\n" + "=" * 70)
