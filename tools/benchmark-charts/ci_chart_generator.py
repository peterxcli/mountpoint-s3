#!/usr/bin/env python3
"""
CI-style chart generator for mountpoint-s3 benchmark results
This script uses the same charting infrastructure as the CI system.
"""

import json
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import webbrowser

def create_ci_format_json():
    """Convert local benchmark results to CI format JSON"""
    
    results_dir = Path("../../results")
    
    # Load the parsed results
    with open(results_dir / 'rand_read_4t_direct_small_parsed.json', 'r') as f:
        parsed_data = json.load(f)
    
    with open(results_dir / 'rand_read_4t_direct_small_peak_mem.json', 'r') as f:
        memory_data = json.load(f)
    
    # Create CI format JSON (similar to what github-action-benchmark expects)
    ci_data = {
        "lastUpdate": "2024-01-01T00:00:00Z",  # Placeholder date
        "repoUrl": "https://github.com/awslabs/mountpoint-s3",
        "entries": {
            "throughput": [
                {
                    "commit": {
                        "id": "local-benchmark",
                        "author": "local-user",
                        "message": "Local benchmark run"
                    },
                    "date": "2024-01-01T00:00:00Z",
                    "tool": "customBiggerIsBetter",
                    "benches": [
                        {
                            "name": parsed_data["name"],
                            "value": parsed_data["value"],
                            "unit": parsed_data["unit"]
                        }
                    ]
                }
            ],
            "memory": [
                {
                    "commit": {
                        "id": "local-benchmark",
                        "author": "local-user", 
                        "message": "Local benchmark run"
                    },
                    "date": "2024-01-01T00:00:00Z",
                    "tool": "customSmallerIsBetter",
                    "benches": [
                        {
                            "name": memory_data["name"],
                            "value": memory_data["value"],
                            "unit": memory_data["unit"]
                        }
                    ]
                }
            ]
        }
    }
    
    return ci_data

def setup_ci_chart_website():
    """Set up the CI chart website locally"""
    
    # Create a temporary directory for the chart website
    temp_dir = tempfile.mkdtemp(prefix="benchmark-charts-")
    
    # Copy the benchmark website files
    website_dir = Path("../../benchmark_website")
    if website_dir.exists():
        for file in website_dir.glob("*"):
            if file.is_file():
                shutil.copy2(file, temp_dir)
    
    # Create the data.js file with our benchmark data
    ci_data = create_ci_format_json()
    with open(os.path.join(temp_dir, "data.js"), 'w') as f:
        f.write(f"window.BENCHMARK_DATA = {json.dumps(ci_data, indent=2)};")
    
    return temp_dir

def create_ci_style_charts():
    """Create charts using the CI infrastructure"""
    
    print("Setting up CI-style chart website...")
    temp_dir = setup_ci_chart_website()
    
    # Create a simple server to serve the charts
    index_path = os.path.join(temp_dir, "index.html")
    
    print(f"Chart website created in: {temp_dir}")
    print(f"Open {index_path} in your browser to view the charts")
    print("\nOr run this command to start a local server:")
    print(f"cd {temp_dir} && python -m http.server 8000")
    print("Then visit: http://localhost:8000")
    
    # Try to open the file in the default browser
    try:
        webbrowser.open(f"file://{os.path.abspath(index_path)}")
        print("\nOpened chart website in your default browser!")
    except:
        print("\nCould not open browser automatically. Please open the file manually.")
    
    return temp_dir

def create_github_action_style_output():
    """Create output.json in the format expected by github-action-benchmark"""
    
    results_dir = Path("../../results")
    
    # Load all parsed results
    parsed_files = list(results_dir.glob("*_parsed.json"))
    
    if not parsed_files:
        print("No parsed JSON files found!")
        return
    
    # Combine all parsed results
    all_results = []
    for file in parsed_files:
        with open(file, 'r') as f:
            data = json.load(f)
            all_results.append(data)
    
    # Create the output.json file
    output_data = {
        "commit": {
            "id": "local-benchmark",
            "author": "local-user",
            "message": "Local benchmark run"
        },
        "benches": all_results
    }
    
    with open(results_dir / "output.json", 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("Created output.json in CI format")
    print("This file can be used with github-action-benchmark")

def main():
    """Main function to generate CI-style charts"""
    
    print("Mountpoint-S3 CI-Style Chart Generator")
    print("=" * 50)
    
    # Check if required files exist
    results_dir = Path("../../results")
    required_files = [
        results_dir / "rand_read_4t_direct_small_parsed.json",
        results_dir / "rand_read_4t_direct_small_peak_mem.json"
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        print(f"Missing required files: {missing_files}")
        print("Please run the benchmark first to generate these files.")
        return
    
    print("Found benchmark results files!")
    
    # Create CI format output
    create_github_action_style_output()
    
    # Create CI-style charts
    chart_dir = create_ci_style_charts()
    
    print("\n" + "=" * 50)
    print("Chart generation complete!")
    print(f"Chart files are in: {chart_dir}")
    print("\nThe charts use the same infrastructure as the CI system.")
    print("You can view them by opening the index.html file in your browser.")

if __name__ == "__main__":
    main() 