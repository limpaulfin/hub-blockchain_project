from pathlib import Path
import datetime
from src.cli import parse_arguments
from src.validator import validate_and_convert_args
from src.orchestrator import execute_search
from src.printer import format_results, save_results, display_results, print_save_confirmation
from src.config import OUTPUT_FILE_LIMIT
from src.file_utils import manage_output_directory

def main():
    """
    The main entry point for the Tuc Mãng Minh tool.
    """
    # 1. Get raw arguments from command line
    raw_args = parse_arguments()

    # 2. Validate and convert arguments
    config, error = validate_and_convert_args(raw_args)
    if error:
        print(f"Error: {error}")
        return

    # This initial header is now part of the formatted_output
    # print("--- Tuc Mãng Minh: History Search ---")
    # print(f"File: {config['file_path']}")
    # print(f"History Path: {config['history_path']}")
    
    # 3. Execute the core logic
    filtered_versions, search_results, exec_error = execute_search(config)

    # 4. Format results
    formatted_output = format_results(
        filtered_versions, 
        search_results, 
        config,
        exec_error
    )

    # 5. Display results in console
    display_results(formatted_output)

    # 6. Save results to file ONLY if there are results
    has_versions = bool(filtered_versions)
    has_matches = bool(search_results)

    # We save if we found versions (when not searching text) 
    # OR if we found matches (when searching text).
    if has_versions or has_matches:
        output_dir = Path('.cursor/rules/tuc-mang-minh/tmp')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up old files before saving the new one
        manage_output_directory(output_dir, OUTPUT_FILE_LIMIT)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"output-{timestamp}.txt"
        output_path = output_dir / output_filename
        
        if save_results(formatted_output, output_path):
            loc = len(formatted_output.splitlines())
            print_save_confirmation(output_path, loc)
        else:
            # Error is printed by save_results
            pass


if __name__ == "__main__":
    main()
