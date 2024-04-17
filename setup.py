# setup.py

import sys
import os

# Get the path to the project directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Assuming setup.py is in the root folder

# Add project directory and 'src' directory to Python path
sys.path.append(project_dir)
sys.path.append(os.path.join(project_dir, 'src'))  # Add 'src' directory to Python path
