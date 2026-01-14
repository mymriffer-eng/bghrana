import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/home/bghranac/repositories/bghrana')

# Read the last lines from passenger.log
log_file = '/home/bghranac/repositories/bghrana/tmp/log/passenger.log'

try:
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    # Find the last Traceback
    traceback_indices = []
    for i, line in enumerate(lines):
        if 'Traceback' in line:
            traceback_indices.append(i)
    
    if traceback_indices:
        # Get the last traceback
        last_idx = traceback_indices[-1]
        # Print 50 lines from the last traceback
        print("=== LAST ERROR ===")
        print(''.join(lines[last_idx:min(last_idx+50, len(lines))]))
    else:
        print("No tracebacks found. Last 20 lines:")
        print(''.join(lines[-20:]))
        
except FileNotFoundError:
    print(f"Log file not found: {log_file}")
except Exception as e:
    print(f"Error reading log: {e}")
