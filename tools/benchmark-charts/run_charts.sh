#!/bin/bash

# Mountpoint-S3 Chart Generator Runner
# This script runs both custom and CI-style chart generators

echo "Mountpoint-S3 Chart Generator"
echo "============================"

# Check if we're in the tools/benchmark-charts directory
if [ ! -f "chart_generator.py" ]; then
    echo "Error: Please run this script from the tools/benchmark-charts directory"
    exit 1
fi

# Check if required files exist in results directory
if [ ! -f "../../results/rand_read_4t_direct_small_parsed.json" ]; then
    echo "Error: Please run the benchmark first to generate results files"
    echo "Make sure you have benchmark results files in the results directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "1. Generating custom charts..."
python chart_generator.py

echo ""
echo "2. Generating CI-style charts..."
python ci_chart_generator.py

echo ""
echo "✅ Chart generation complete!"
echo ""
echo "📊 Custom charts created in ../../results/:"
echo "   - benchmark_performance_chart.png"
echo "   - benchmark_summary.png" 
echo "   - benchmark_iteration_analysis.png"
echo "   - dashboard.html"
echo ""
echo "🌐 CI-style charts opened in browser"
echo ""
echo "You can view the custom dashboard by opening ../../results/dashboard.html in your browser" 