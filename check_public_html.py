#!/usr/bin/env python
import os

print("=" * 60)
print("Checking public_html directory")
print("=" * 60)

public_html = '/home/bghranac/public_html'

print(f"\nContents of {public_html}:")
try:
    files = os.listdir(public_html)
    for f in sorted(files):
        filepath = os.path.join(public_html, f)
        if os.path.isdir(filepath):
            print(f"  [DIR]  {f}")
        else:
            size = os.path.getsize(filepath)
            print(f"  [FILE] {f} ({size} bytes)")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Checking .htaccess content:")
print("=" * 60)

htaccess_path = os.path.join(public_html, '.htaccess')
try:
    with open(htaccess_path, 'r') as f:
        content = f.read()
    print(content)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Python App should be configured to use:")
print(f"Document Root: {public_html}")
print("Application Root: /home/bghranac/repositories/bghrana")
print("=" * 60)
