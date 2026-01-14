#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check logs for registration errors
"""

import os

log_file = '/home/bghranac/repositories/bghrana/passenger.log'

print("=" * 70)
print("CHECKING PASSENGER LOG FOR REGISTRATION ERRORS")
print("=" * 70)

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Get last 100 lines
    last_lines = lines[-100:] if len(lines) > 100 else lines
    
    print("\nLast 100 lines of passenger.log:")
    print("-" * 70)
    print(''.join(last_lines))
else:
    print(f"\n✗ Log file not found: {log_file}")

print("\n" + "=" * 70)
print("Look for errors related to:")
print("  - Email sending (SMTP)")
print("  - Database errors")
print("  - Allauth issues")
print("=" * 70)
