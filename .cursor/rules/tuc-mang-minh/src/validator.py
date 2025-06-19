import os
from datetime import datetime
from pathlib import Path
from .config import COMMON_HISTORY_PATHS

def _find_valid_history_path(initial_path: str | None) -> str | None:
    """
    Checks for a valid history path, trying alternatives if the initial one fails.
    Returns the valid path or None if no valid path is found.
    """
    # 1. If a specific path is provided via argument, check it first.
    if initial_path:
        path_to_check = Path(initial_path).expanduser().resolve()
        if path_to_check.is_dir():
            return str(path_to_check)

    # 2. If no path is provided or the provided path is invalid,
    #    check the list of common, hard-coded paths from the config.
    for path_str in COMMON_HISTORY_PATHS:
        path = Path(path_str).expanduser().resolve()
        if path.is_dir():
            return str(path)
            
    # 3. If no path is found, return None
    return None


def validate_and_convert_args(args):
    """
    Validates arguments and converts them to the correct types.
    It now intelligently finds the history path.

    Args:
        args: The raw arguments object from argparse.

    Returns:
        A tuple containing a dictionary of validated config and an error string.
        If validation is successful, the error string is None.
    """
    config = {}
    
    # Find the correct history path from a list of possibilities
    valid_history_path = _find_valid_history_path(args.history_path)

    if not valid_history_path:
        error_message = (
            f"Could not automatically find a valid history directory.\n\n"
            f"Checked common locations like '~/.config/Cursor/User/History'.\n\n"
            "Please ensure Local History is enabled in VS Code/Cursor, or specify a valid path using the --history-path argument."
        )
        return None, error_message
    
    config['history_path'] = valid_history_path

    config['file_path'] = args.file_path
    config['text'] = args.text

    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None, "Invalid start_date format. Please use 'YYYY-MM-DD HH:MM:SS'."
    config['start_date'] = start_date

    end_date = None
    if args.end_date:
        try:
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None, "Invalid end_date format. Please use 'YYYY-MM-DD HH:MM:SS'."
    config['end_date'] = end_date

    if args.context < 0:
        return None, "Context must be a non-negative integer."
    config['context'] = args.context

    if args.limit is not None and args.limit <= 0:
        return None, "Limit must be a positive integer."
    config['limit'] = args.limit

    return config, None
