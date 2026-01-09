import os
import sys

print("=" * 50)
print("ENVIRONMENT VARIABLES TEST")
print("=" * 50)
print(f"DB_USER: {os.environ.get('DB_USER', 'NOT SET')}")
print(f"DB_NAME: {os.environ.get('DB_NAME', 'NOT SET')}")
print(f"DB_HOST: {os.environ.get('DB_HOST', 'NOT SET')}")
print(f"DB_PORT: {os.environ.get('DB_PORT', 'NOT SET')}")
print(f"Password length: {len(os.environ.get('DB_PASSWORD', ''))}")
print(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
print("=" * 50)

# Test PyMySQL connection
print("\nTesting PyMySQL connection...")
try:
    import pymysql
    conn = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', ''),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', ''),
        port=int(os.environ.get('DB_PORT', '3306'))
    )
    print("✓ SUCCESS! MySQL connection works!")
    conn.close()
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)
