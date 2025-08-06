#!/bin/bash

# CI-Style Chart Generator for Mountpoint-S3 Benchmark Results
# This script uses the same charting infrastructure as the CI system

echo "Mountpoint-S3 CI-Style Chart Generator"
echo "======================================"

# Check if we're in the tools/benchmark-charts directory
if [ ! -f "ci_chart_generator.py" ]; then
    echo "Error: Please run this script from the tools/benchmark-charts directory"
    exit 1
fi

# Check if required files exist in results directory
if [ ! -f "../../results/rand_read_4t_direct_small_parsed.json" ]; then
    echo "Error: Please run the benchmark first to generate results files"
    echo "Make sure you have benchmark results files in the results directory"
    exit 1
fi

# Run the CI-style chart generator
python3 ci_chart_generator.py

echo ""
echo "Done! The charts should have opened in your browser."
echo "If not, check the output above for the chart directory location." 