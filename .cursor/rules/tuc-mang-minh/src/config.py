from pathlib import Path

# This file contains default configurations for the tool.

# We assume the script is run from the project's root directory.
# The .history folder is expected to be in this root.
# PROJECT_ROOT = Path(os.getcwd())

# Define the common paths for Local History directories.
# This makes the tool more robust across different machine setups.
home_dir = Path.home()
COMMON_HISTORY_PATHS = [
    str(home_dir / ".config/Cursor/User/History"),  # [Priority 1] Standard for Cursor (capital 'C')
    str(home_dir / ".config/cursor/User/History"),  # [Priority 2] Fallback for lowercase 'c'
    str(home_dir / ".config/Code/User/History"),    # [Priority 3] Standard for VS Code
]

# Maximum number of output files to keep in the tmp directory.
OUTPUT_FILE_LIMIT = 100 