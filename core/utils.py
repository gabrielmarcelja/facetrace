"""
Utility Functions
Export, browser opening, and other helpers
"""

import json
import csv
import webbrowser
import time
from typing import List, Dict
from pathlib import Path


def export_results(results: List[Dict], output_file: str):
    """
    Export results to file (JSON or CSV)

    Args:
        results: List of match dictionaries
        output_file: Output file path (.json or .csv)
    """
    output_path = Path(output_file)
    extension = output_path.suffix.lower()

    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if extension == '.json':
        _export_json(results, output_path)
    elif extension == '.csv':
        _export_csv(results, output_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}. Use .json or .csv")


def _export_json(results: List[Dict], output_path: Path):
    """Export results to JSON file"""
    data = {
        'total_matches': len(results),
        'matches': results
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _export_csv(results: List[Dict], output_path: Path):
    """Export results to CSV file"""
    fieldnames = ['platform', 'score', 'username', 'url']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # Write data rows if there are results
        for result in results:
            writer.writerow({
                'platform': result['platform'],
                'score': result['score'],
                'username': result.get('username', ''),
                'url': result['url']
            })


def open_in_browser(matches: List[Dict]):
    """
    Open match URLs in default browser with delay between opens

    Args:
        matches: List of match dictionaries
    """
    for i, match in enumerate(matches):
        url = match['url']
        try:
            webbrowser.open(url)
            # Add delay between opens to avoid browser overload (except for last one)
            if i < len(matches) - 1:
                time.sleep(0.5)
        except Exception:
            pass  # Silently fail if browser can't open

