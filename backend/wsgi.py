# backend/wsgi.py
import os
import sys

# Absolute import is correct here when run by Gunicorn in /app
from .create_app import create_app

print("wsgi.py: Calling create_app()...", file=sys.stderr)
app = create_app()
print("wsgi.py: create_app() returned. 'app' object created.", file=sys.stderr)

# This part is mostly for running locally with `python wsgi.py`
if __name__ == "__main__":
    print("wsgi.py running in __main__", file=sys.stderr)
    # Use environment variable for port or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Debug should be controlled by FLASK_DEBUG env var set in Config
    app.run(host='0.0.0.0', port=port)