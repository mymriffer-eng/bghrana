import os
import sys

# Logging for debugging
import logging
logging.basicConfig(
    filename='/home/bghranac/passenger_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

try:
    logging.info("=" * 60)
    logging.info("Passenger WSGI starting...")
    
    # Add project directory to the sys.path
    project_dir = os.path.dirname(__file__)
    sys.path.insert(0, project_dir)
    logging.info(f"Project directory: {project_dir}")
    logging.info(f"Python path: {sys.path[:3]}")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'products.settings')
    logging.info(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Import Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    logging.info("✓ Django WSGI application loaded successfully")
    logging.info("=" * 60)
    
except Exception as e:
    logging.error(f"✗ ERROR loading Django: {e}")
    logging.exception("Full traceback:")
    raise
