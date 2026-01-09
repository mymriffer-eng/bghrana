#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Reset Git repository to match remote origin/master.
This will discard local changes and pull fresh from GitHub.
"""

import subprocess
import os

# Change to repository directory
os.chdir('/home/bghranac/repositories/bghrana')

commands = [
    # Remove untracked files
    ['git', 'clean', '-fd'],
    
    # Reset all local changes
    ['git', 'reset', '--hard', 'HEAD'],
    
    # Fetch latest from remote
    ['git', 'fetch', 'origin'],
    
    # Reset to remote master
    ['git', 'reset', '--hard', 'origin/master'],
    
    # Show current status
    ['git', 'status'],
]

print("Resetting Git repository to match GitHub remote...")
print("=" * 60)

for cmd in commands:
    print(f"\nRunning: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

print("=" * 60)
print("✓ Git reset complete")
print("\nNext step: Restart Python App in cPanel")
