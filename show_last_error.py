#!/home/bghranac/virtualenv/repositories/bghrana/3.11/bin/python
"""
Show last error from passenger log after registration attempt
"""

import os
from datetime import datetime

log_file = '/home/bghranac/repositories/bghrana/passenger.log'

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Find last Traceback
    for i in range(len(lines) - 1, -1, -1):
        if 'Traceback' in lines[i]:
            # Print from Traceback to end
            print(''.join(lines[i:]))
            break
else:
    print(f"Log file not found: {log_file}")
