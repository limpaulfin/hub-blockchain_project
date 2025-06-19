from .history_finder import find_versions, filter_versions_by_date
from .content_searcher import search_in_version

def execute_search(config: dict):
    """
    Orchestrates the main logic of finding, filtering, and searching.

    Args:
        config: A dictionary with validated configuration.

    Returns:
        A tuple containing the list of filtered versions and a dictionary
        mapping version paths to search matches.
    """
    # 1. Find all versions
    all_versions = find_versions(config['history_path'], config['file_path'])
    if not all_versions:
        return [], {}, "No historical versions found for this file."

    # Apply limit to the most recent versions
    if config['limit'] and len(all_versions) > config['limit']:
        all_versions = all_versions[:config['limit']]

    # 2. Filter by date
    filtered_list = filter_versions_by_date(
        all_versions, config['start_date'], config['end_date']
    )
    if not filtered_list:
        return [], {}, "No versions found in the specified time range."
    
    # 3. Search for text if provided
    search_results = {}
    if config['text']:
        for version in filtered_list:
            matches = search_in_version(version['path'], config['text'], config['context'])
            if matches:
                search_results[version['path']] = {
                    'timestamp': version['timestamp'],
                    'matches': matches
                }
    
    return filtered_list, search_results, None 