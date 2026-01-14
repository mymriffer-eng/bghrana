#!/usr/bin/env python
"""
Show last error from passenger log - paste entire script into cPanel
"""
import os

log_paths = [
    '/home/bghranac/repositories/bghrana/tmp/log/passenger.log',
    '/home/bghranac/logs/bghrana.com.error.log',
    '/home/bghranac/tmp/error_log',
]

print("=" * 70)
print("SEARCHING FOR ERROR LOGS")
print("=" * 70)

found_logs = []
for log_path in log_paths:
    if os.path.exists(log_path):
        found_logs.append(log_path)
        print(f"✓ Found: {log_path}")
    else:
        print(f"✗ Not found: {log_path}")

if not found_logs:
    print("\n! No log files found")
    print("\nTry checking in cPanel:")
    print("  - Metrics → Errors")
    print("  - File Manager → /home/bghranac/logs/")
else:
    for log_path in found_logs:
        print(f"\n{'=' * 70}")
        print(f"READING: {log_path}")
        print("=" * 70)
        
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Find all tracebacks
            traceback_indices = [i for i, line in enumerate(lines) if 'Traceback' in line]
            
            if traceback_indices:
                # Show last traceback
                last_idx = traceback_indices[-1]
                print(f"\n=== LAST ERROR (showing from line {last_idx}) ===\n")
                error_lines = lines[max(0, last_idx-5):min(last_idx+50, len(lines))]
                print(''.join(error_lines))
            else:
                # Show last 30 lines
                print("\n=== LAST 30 LINES ===\n")
                print(''.join(lines[-30:]))
                
        except Exception as e:
            print(f"Error reading {log_path}: {e}")

print("\n" + "=" * 70)
