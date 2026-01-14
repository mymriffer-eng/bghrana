#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Force Git reset - upload this file directly to /home/bghranac/
Run it to discard ALL local changes and sync with GitHub.
"""

import subprocess
import os

repo_path = '/home/bghranac/repositories/bghrana'

print("=" * 70)
print("FORCE GIT RESET - Syncing with GitHub")
print("=" * 70)

# Change to repository directory
try:
    os.chdir(repo_path)
    print(f"✓ Changed to: {os.getcwd()}")
except Exception as e:
    print(f"✗ ERROR: Cannot access {repo_path}: {e}")
    exit(1)

# Commands to force reset
commands = [
    (['git', 'fetch', 'origin'], "Fetching from GitHub..."),
    (['git', 'reset', '--hard', 'origin/master'], "Resetting to origin/master..."),
    (['git', 'clean', '-fd'], "Removing untracked files..."),
    (['git', 'status'], "Final status:"),
]

for cmd, description in commands:
    print(f"\n{description}")
    print(f"Command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=repo_path
        )
        print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            print(f"✗ Command failed with exit code {result.returncode}")
    except Exception as e:
        print(f"✗ ERROR: {e}")

print("\n" + "=" * 70)
print("✓ COMPLETE - Repository synced with GitHub")
print("=" * 70)
print("\nNEXT STEPS:")
print("1. Go to cPanel Python App interface")
print("2. Click 'RESTART' button")
print("3. Wait 20 seconds")
print("4. Test: https://bghrana.com")
