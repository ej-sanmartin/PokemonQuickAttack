"""Rate limiting configuration for the Flask application."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_rate_limiter(app):
    """Initialize rate limiter for the Flask application.
    
    Args:
        app: Flask application instance
    """
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Store limiter in app context for access in routes
    app.limiter = limiter
    
    return limiter 