#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check if forms.py has the fix
"""

import os

forms_file = '/home/bghranac/repositories/bghrana/catalog/forms.py'

print("=" * 70)
print("CHECKING catalog/forms.py FOR FIX")
print("=" * 70)

if os.path.exists(forms_file):
    with open(forms_file, 'r') as f:
        content = f.read()
    
    print("\nSearching for clean() method override...")
    
    if 'def clean(self):' in content and 'Skip UserCreationForm' in content:
        print("✓ FIX IS PRESENT - clean() method override found")
    else:
        print("✗ FIX IS NOT PRESENT - clean() method override NOT found")
    
    print("\nShowing CustomUserCreationForm section (lines around clean):")
    print("-" * 70)
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'class CustomUserCreationForm' in line:
            # Show 40 lines after class declaration
            for j in range(i-1, min(i+39, len(lines))):
                print(f"{j+1}: {lines[j]}")
            break
    
    # Touch restart file
    print("\n" + "=" * 70)
    print("FORCING RESTART")
    print("=" * 70)
    repo_path = '/home/bghranac/repositories/bghrana'
    restart_file = os.path.join(repo_path, 'tmp', 'restart.txt')
    os.makedirs(os.path.dirname(restart_file), exist_ok=True)
    with open(restart_file, 'a'):
        os.utime(restart_file, None)
    print(f"✓ Touched {restart_file}")
    print("\nWait 15 seconds then test registration again")
else:
    print(f"✗ File not found: {forms_file}")
