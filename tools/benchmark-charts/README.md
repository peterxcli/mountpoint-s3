# Mountpoint-S3 Benchmark Results Visualization

This directory contains tools to visualize your benchmark results with interactive charts and dashboards.

## Files Created

- `chart_generator.py` - Python script to generate custom charts from benchmark data
- `ci_chart_generator.py` - Python script that uses the same CI infrastructure for charts
- `generate_ci_charts.sh` - Shell script to easily run CI-style charts
- `requirements.txt` - Python dependencies needed for chart generation
- `dashboard.html` - Interactive HTML dashboard to view results
- `README.md` - This file
- `CHART_COMPARISON.md` - Detailed comparison of chart options

## Quick Start

### Option 1: Custom Charts (Recommended for detailed analysis)
1. **Install Python dependencies:**
   ```bash
   cd tools/benchmark-charts
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Generate custom charts:**
   ```bash
   python chart_generator.py
   ```

3. **View the dashboard:**
   ```bash
   # Open in your web browser
   open ../results/dashboard.html
   # Or use a simple HTTP server
   cd ../results && python -m http.server 8000
   # Then visit http://localhost:8000/dashboard.html
   ```

### Option 2: CI-Style Charts (Same as CI system)
1. **Generate CI-style charts:**
   ```bash
   cd tools/benchmark-charts
   ./generate_ci_charts.sh
   ```
   
   This will automatically open the charts in your browser using the same infrastructure as the CI system.

### Option 3: Run Both (Recommended)
```bash
cd tools/benchmark-charts
./run_charts.sh
```

This will generate both custom charts and CI-style charts in one command.

## What You'll Get

### Custom Charts (chart_generator.py)
The script generates three types of charts:

#### 1. Comprehensive Performance Chart (`../results/benchmark_performance_chart.png`)
- Throughput over iterations
- IOPS over iterations  
- Latency over iterations
- Summary metrics comparison

#### 2. Simple Summary Chart (`../results/benchmark_summary.png`)
- Performance vs Memory usage comparison
- Pie chart showing the ratio

#### 3. Iteration Analysis Chart (`../results/benchmark_iteration_analysis.png`)
- Detailed throughput analysis with statistics
- IOPS analysis with standard deviation
- Latency analysis with trends
- Throughput vs Latency correlation

### CI-Style Charts (ci_chart_generator.py)
Uses the exact same charting infrastructure as the CI system:
- Interactive web-based charts
- Same styling and functionality as the official benchmark website
- Professional appearance matching the CI charts
- Automatic browser opening

## Dashboard Features

The HTML dashboard provides:
- **Real-time metrics display** - Shows throughput, memory usage, IOPS, and latency
- **Interactive tabs** - Switch between different chart views
- **Responsive design** - Works on desktop and mobile
- **Automatic data loading** - Reads directly from your JSON files

## Data Sources

The charts are generated from:
- `../results/rand_read_4t_direct_small_parsed.json` - Summary throughput data
- `../results/rand_read_4t_direct_small_peak_mem.json` - Memory usage data
- `../results/rand_read_4t_direct_small_iter*.json` - Detailed iteration data (10 files)

## Customization

You can modify `chart_generator.py` to:
- Change chart colors and styles
- Add new metrics or visualizations
- Adjust chart sizes and layouts
- Export in different formats (PDF, SVG, etc.)

## Troubleshooting

- **Missing dependencies**: Run `pip install -r requirements.txt` in the virtual environment
- **Charts not showing**: Make sure you're running the script from the tools/benchmark-charts directory
- **Dashboard not loading**: Check that all JSON files are present in the results directory
- **Virtual environment issues**: Delete the `venv` directory and recreate it with `python3 -m venv venv` 