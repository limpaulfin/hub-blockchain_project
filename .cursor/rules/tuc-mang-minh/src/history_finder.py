import os
import json
from datetime import datetime
from pathlib import Path

def find_versions(history_dir: str, file_path_to_find: str):
    """
    Finds all historical versions of a file by scanning the real
    VSCode/Cursor Local History storage.
    
    This function iterates through the hashed subdirectories in the history path,
    reads the `entries.json` metadata file in each, and matches the
    original file path to find its historical versions.
    """
    versions = []
    history_path = Path(history_dir)
    file_path_to_find_abs = str(Path(file_path_to_find).resolve())

    if not history_path.is_dir():
        return []

    # Iterate over each hashed subdirectory in the history storage
    for entry in history_path.iterdir():
        if entry.is_dir():
            metadata_file = entry / 'entries.json'
            if metadata_file.is_file():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    # Check if this directory is for the file we are looking for
                    if metadata.get("resource") != f"file://{file_path_to_find_abs}":
                        continue

                    # If it matches, extract all versions from the metadata
                    for version_entry in metadata.get("entries", []):
                        version_filename = version_entry.get("id")
                        version_timestamp_ms = version_entry.get("timestamp")
                        
                        if version_filename and version_timestamp_ms:
                            version_path = entry / version_filename
                            if version_path.is_file():
                                versions.append({
                                    "path": str(version_path),
                                    "timestamp": datetime.fromtimestamp(version_timestamp_ms / 1000)
                                })
                    
                    # Found the correct history directory, no need to check others
                    break

                except (json.JSONDecodeError, IOError):
                    continue
    
    return sorted(versions, key=lambda v: v['timestamp'])

def filter_versions_by_date(versions: list, start_date: datetime, end_date: datetime):
    """
    Filters a list of file versions by a date range.

    Args:
        versions: A list of file version dictionaries.
        start_date: The start of the date range. Can be None.
        end_date: The end of the date range. Can be None.

    Returns:
        A filtered list of file version dictionaries.
    """
    if not start_date and not end_date:
        return versions

    filtered_versions = []
    for version in versions:
        is_after_start = not start_date or version['timestamp'] >= start_date
        is_before_end = not end_date or version['timestamp'] <= end_date
        if is_after_start and is_before_end:
            filtered_versions.append(version)
            
    return filtered_versions 