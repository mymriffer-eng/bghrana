#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Install all dependencies from requirements.txt
"""

import subprocess
import os

repo_path = '/home/bghranac/repositories/bghrana'
pip_path = '/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/pip'
requirements_file = os.path.join(repo_path, 'requirements.txt')

print("=" * 70)
print("INSTALLING DEPENDENCIES FROM requirements.txt")
print("=" * 70)

# Check if requirements.txt exists
if not os.path.exists(requirements_file):
    print(f"✗ ERROR: {requirements_file} not found!")
    exit(1)

print(f"\n✓ Found: {requirements_file}")
print(f"✓ Using pip: {pip_path}")

# Install requirements
print("\nInstalling dependencies...")
print("-" * 70)

try:
    result = subprocess.run(
        [pip_path, 'install', '-r', requirements_file],
        capture_output=True,
        text=True,
        cwd=repo_path
    )
    
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("-" * 70)
        print("✓ Installation successful!")
    else:
        print("-" * 70)
        print(f"✗ Installation failed with exit code {result.returncode}")
        exit(1)
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    exit(1)

# Show installed packages
print("\n" + "=" * 70)
print("INSTALLED PACKAGES:")
print("=" * 70)

try:
    result = subprocess.run(
        [pip_path, 'list'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
except Exception as e:
    print(f"Warning: Could not list packages: {e}")

print("\n" + "=" * 70)
print("✓ COMPLETE - All dependencies installed")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Go to cPanel Python App")
print("2. Click 'RESTART' button")
print("3. Wait 20 seconds")
print("4. Test: https://bghrana.com")
