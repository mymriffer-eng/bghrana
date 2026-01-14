#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Pull latest changes from GitHub and verify urls.py
"""

import subprocess
import os

repo_path = '/home/bghranac/repositories/bghrana'
os.chdir(repo_path)

print("=" * 70)
print("SYNCING WITH GITHUB")
print("=" * 70)

# Git pull
print("\nPulling latest changes from GitHub...")
result = subprocess.run(
    ['git', 'pull', 'origin', 'master'],
    capture_output=True,
    text=True,
    cwd=repo_path
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Check urls.py content
print("\n" + "=" * 70)
print("CHECKING products/urls.py")
print("=" * 70)

urls_file = os.path.join(repo_path, 'products', 'urls.py')
if os.path.exists(urls_file):
    with open(urls_file, 'r') as f:
        content = f.read()
    
    if 'static(settings.MEDIA_URL' in content:
        print("\n✓ Media URL pattern found in urls.py")
        print("\nRelevant lines:")
        for i, line in enumerate(content.split('\n'), 1):
            if 'media' in line.lower() or 'static' in line.lower():
                print(f"  {i}: {line}")
    else:
        print("\n✗ Media URL pattern NOT found in urls.py")
        print("\nCurrent urlpatterns section:")
        lines = content.split('\n')
        in_patterns = False
        for line in lines:
            if 'urlpatterns' in line:
                in_patterns = True
            if in_patterns:
                print(f"  {line}")
                if line.strip().startswith(']'):
                    break
else:
    print(f"\n✗ urls.py not found at {urls_file}")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. If media pattern found - Restart Python App")
print("2. If NOT found - We need to fix urls.py on server")
