import argparse

def parse_arguments():
    """Sets up the argument parser and returns the parsed arguments."""
    parser = argparse.ArgumentParser(
        description="A tool to search through file versions from VS Code's Local History."
    )
    
    parser.add_argument(
        'file_path', 
        type=str, 
        help='The original path of the file to search for.'
    )
    parser.add_argument(
        '--text', 
        type=str, 
        help='The text to search for within the file versions.'
    )
    parser.add_argument(
        '--start-date', 
        type=str, 
        help='The start date for the search period (e.g., "YYYY-MM-DD HH:MM:SS").'
    )
    parser.add_argument(
        '--end-date', 
        type=str, 
        help='The end date for the search period (e.g., "YYYY-MM-DD HH:MM:SS").'
    )
    parser.add_argument(
        '--history-path', 
        type=str, 
        default=None, 
        help='(Optional) Path to a specific history directory to search. If not provided, common paths will be checked automatically.'
    )
    parser.add_argument(
        '--context',
        type=int,
        default=5,
        help='Number of lines of context to show before and after the match (default: 5).'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Limit the search to the N most recent versions (default: 50).'
    )

    return parser.parse_args() 