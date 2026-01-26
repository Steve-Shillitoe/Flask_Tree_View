"""
Development entry point for the Flask app.

- Works in Visual Studio 2026 and CLI
- Uses the create_app() factory from AnimalKingdom
- Compatible with Flask-Migrate
- Exposes wsgi_app for IIS / production servers
"""

import os
from AnimalKingdom import create_app

# Create Flask app from factory
app = create_app()

# Expose WSGI app for IIS / wfastcgi if needed
wsgi_app = app.wsgi_app

# Run development server
if __name__ == "__main__":
    # Get host and port from Visual Studio environment variables if set
    HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
    try:
        PORT = int(os.environ.get("SERVER_PORT", 5000))
    except ValueError:
        PORT = 5000

    # Enable debug mode for auto-reload and nicer errors
    app.run(host=HOST, port=PORT, debug=True)
