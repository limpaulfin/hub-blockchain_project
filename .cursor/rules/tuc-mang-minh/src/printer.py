import textwrap
import datetime

def format_results(filtered_versions, search_results, config, initial_error):
    """
    Formats the search results into a string.
    
    Args:
        filtered_versions: The list of versions that were searched.
        search_results: A dictionary of matches found.
        config: A dictionary containing all validated search parameters.
        initial_error: An initial error message from the orchestrator.
        
    Returns:
        A string containing the formatted results.
    """
    file_path = config.get('file_path')
    history_path = config.get('history_path')
    search_text = config.get('text')
    start_date = config.get('start_date')
    end_date = config.get('end_date')

    output_lines = []
    output_lines.append("--- Túc Mạng Minh: History Search ---")
    output_lines.append(f"Search Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"File: {file_path}")
    output_lines.append(f"History Path: {history_path}")

    if search_text:
        output_lines.append(f"Search Text: '{search_text}'")

    if start_date or end_date:
        start_str = start_date.strftime('%Y-%m-%d %H:%M:%S') if start_date else "Beginning of time"
        end_str = end_date.strftime('%Y-%m-%d %H:%M:%S') if end_date else "Present"
        output_lines.append(f"Date Range: {start_str} -> {end_str}")

    if initial_error:
        output_lines.append(initial_error)
        return "\n".join(output_lines)

    if not search_text:
        output_lines.append(f"Found {len(filtered_versions)} historical versions.")
        output_lines.append("-----------------------------------------")
        for version in filtered_versions:
            output_lines.append(f"Version: {version['path']}")
            output_lines.append(f"Timestamp: {version['timestamp']}")
            output_lines.append("-----------------------------------------")
        output_lines.append(f"\nSearch complete. Listed {len(filtered_versions)} versions.")
        return "\n".join(output_lines)

    output_lines.append(f"Found {len(filtered_versions)} versions to search...")
    output_lines.append("-----------------------------------------")

    if not search_results:
        output_lines.append(f"No results found for '{search_text}'.")
    else:
        for path, result in search_results.items():
            output_lines.append(f"Found matches in: {path}")
            output_lines.append(f"Timestamp: {result['timestamp']}")
            for match in result['matches']:
                output_lines.append("...")
                for line_num, line_content in match['context_before']:
                    output_lines.append(f"{line_num:4d} | {line_content}")
                
                output_lines.append(f">{match['line_num']:4d} | {match['line'].strip()}")

                for line_num, line_content in match['context_after']:
                    output_lines.append(f"{line_num:4d} | {line_content}")
            output_lines.append("=========================================")
        output_lines.append(f"\nSearch complete. Found {len(search_results)} files with matches.")

    return "\n".join(output_lines)

def display_results(formatted_string):
    """Prints the formatted results to the console."""
    print(formatted_string)

def save_results(formatted_string, filepath):
    """Saves the formatted results to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_string)
        return True
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
        return False

def print_save_confirmation(output_path, loc):
    """Prints the save confirmation message, with tips for large files."""
    print(f"\n--- Also saved to: {output_path} ({loc} lines) ---")
    
    tip_message = f"""
    💡 Tip: The output file can be large. You can read it in chunks or filter it:
       - Read first 200 lines: `head -n 200 "{output_path}"`
       - Read last 200 lines: `tail -n 200 "{output_path}"`
       - Read lines 201-400: `sed -n '201,400p' "{output_path}"`
       - Filter for a keyword: `grep 'your_keyword' "{output_path}"`
    """
    print(textwrap.dedent(tip_message)) 