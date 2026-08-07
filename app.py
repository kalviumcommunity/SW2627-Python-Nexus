import os
import sys
from pathlib import Path

# Ensure Dashboard directory is on python path
dashboard_dir = Path(__file__).parent / "Dashboard"
if str(dashboard_dir) not in sys.path:
    sys.path.insert(0, str(dashboard_dir))

# Change directory context to Dashboard if executing root app.py
os.chdir(dashboard_dir)

# Import and run main application from Dashboard/app.py
import app as dashboard_app