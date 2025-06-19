from pathlib import Path

def manage_output_directory(output_dir: Path, limit: int):
    """
    Ensures the number of files in the output directory does not exceed the limit.
    Deletes the oldest files if necessary.
    """
    if not output_dir.is_dir():
        return

    # Files are named like 'output-YYYYMMDD_HHMMSS.txt', so sorting alphabetically works
    files = sorted(output_dir.glob('output-*.txt'))
    
    if len(files) >= limit:
        num_to_delete = len(files) - limit + 1
        for i in range(num_to_delete):
            files[i].unlink() 