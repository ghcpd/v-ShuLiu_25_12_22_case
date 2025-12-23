#!/usr/bin/env python3
"""
Performance validation script.
"""

import time
from user_display_optimized import display_users, filter_users, get_user_by_id, sample_users

# Generate larger test set
large_users = sample_users * 500  # 50,000 users

# Test display performance
start = time.time()
result = display_users(large_users, verbose=False)
display_time = time.time() - start

# Test filter performance
start = time.time()
filtered = filter_users(large_users, {'status': 'Active'})
filter_time = time.time() - start

# Test lookup performance
start = time.time()
user = get_user_by_id(large_users, 25000)
lookup_time = time.time() - start

print(f'Display 50,000 users: {display_time:.3f}s (target: <0.120s) - {"✅" if display_time < 0.120 else "❌"}')
print(f'Filter 50,000 users: {filter_time:.3f}s (target: <0.015s) - {"✅" if filter_time < 0.015 else "❌"}')
print(f'ID lookup: {lookup_time:.6f}s (target: <0.0005s) - {"✅" if lookup_time < 0.0005 else "❌"}')
print(f'Filtered {len(filtered)} users')