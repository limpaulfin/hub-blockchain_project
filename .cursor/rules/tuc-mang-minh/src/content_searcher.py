def search_in_version(file_path: str, search_text: str, context_lines: int = 0):
    """
    Searches for a string within a single file and captures context lines.

    Args:
        file_path: The path to the file to search in.
        search_text: The text to search for.
        context_lines: The number of context lines to capture before and after the match.

    Returns:
        A list of dictionaries, where each dictionary contains the line number,
        the matching line, and the context lines.
    """
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if search_text in line:
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    
                    context_before = [(start + j + 1, lines[start + j].strip()) for j in range(i - start)]
                    match_line = line.strip()
                    context_after = [(i + j + 2, lines[i + 1 + j].strip()) for j in range(end - (i + 1))]

                    matches.append({
                        "line_num": i + 1,
                        "line": match_line,
                        "context_before": context_before,
                        "context_after": context_after
                    })
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
    
    return matches 