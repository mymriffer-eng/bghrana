#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Check latest errors in passenger log
"""

import os

log_file = '/home/bghranac/repositories/bghrana/passenger.log'

print("=" * 70)
print("LATEST ERRORS IN PASSENGER LOG")
print("=" * 70)

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Get last 150 lines to see full traceback
    last_lines = lines[-150:]
    
    # Find the last error
    error_start = -1
    for i in range(len(last_lines) - 1, -1, -1):
        if 'Traceback' in last_lines[i]:
            error_start = i
            break
    
    if error_start >= 0:
        print("\nLast error traceback:")
        print("-" * 70)
        print(''.join(last_lines[error_start:]))
    else:
        print("\nNo recent traceback found. Last 50 lines:")
        print("-" * 70)
        print(''.join(last_lines[-50:]))
else:
    print(f"\n✗ Log file not found: {log_file}")
