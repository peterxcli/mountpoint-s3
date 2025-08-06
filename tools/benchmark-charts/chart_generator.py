#!/usr/bin/env python3
"""
Chart generator for mountpoint-s3 benchmark results
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
import seaborn as sns
import os

# Set style for better looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_parsed_results():
    """Load the parsed benchmark results"""
    results_dir = Path("../../results")
    with open(results_dir / 'rand_read_4t_direct_small_parsed.json', 'r') as f:
        return json.load(f)

def load_memory_results():
    """Load the memory usage results"""
    results_dir = Path("../../results")
    with open(results_dir / 'rand_read_4t_direct_small_peak_mem.json', 'r') as f:
        return json.load(f)

def load_iteration_data():
    """Load data from all iteration files"""
    results_dir = Path("../../results")
    iterations = []
    for i in range(1, 11):  # 10 iterations
        filename = results_dir / f'rand_read_4t_direct_small_iter{i}.json'
        if filename.exists():
            with open(filename, 'r') as f:
                data = json.load(f)
                # Extract throughput from the job results
                if 'jobs' in data and len(data['jobs']) > 0:
                    job = data['jobs'][0]
                    if 'read' in job:
                        # Convert bandwidth from KB/s to MiB/s
                        bw_kb = job['read']['bw']
                        bw_mib = bw_kb / 1024  # Convert KB/s to MiB/s
                        iterations.append({
                            'iteration': i,
                            'throughput_mib': bw_mib,
                            'iops': job['read']['iops'],
                            'latency_mean_ms': job['read']['clat_ns']['mean'] / 1_000_000  # Convert ns to ms
                        })
    return iterations

def create_performance_chart():
    """Create a comprehensive performance chart"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Load data
    parsed_data = load_parsed_results()
    memory_data = load_memory_results()
    iterations = load_iteration_data()
    
    # Chart 1: Throughput over iterations
    iterations_data = [it['iteration'] for it in iterations]
    throughput_data = [it['throughput_mib'] for it in iterations]
    
    ax1.plot(iterations_data, throughput_data, 'o-', linewidth=2, markersize=8)
    ax1.set_title('Throughput Over Iterations', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Throughput (MiB/s)')
    ax1.grid(True, alpha=0.3)
    
    # Add average line
    avg_throughput = np.mean(throughput_data)
    ax1.axhline(y=avg_throughput, color='red', linestyle='--', alpha=0.7, 
                label=f'Average: {avg_throughput:.2f} MiB/s')
    ax1.legend()
    
    # Chart 2: IOPS over iterations
    iops_data = [it['iops'] for it in iterations]
    ax2.plot(iterations_data, iops_data, 's-', linewidth=2, markersize=8, color='green')
    ax2.set_title('IOPS Over Iterations', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('IOPS')
    ax2.grid(True, alpha=0.3)
    
    # Add average line
    avg_iops = np.mean(iops_data)
    ax2.axhline(y=avg_iops, color='red', linestyle='--', alpha=0.7,
                label=f'Average: {avg_iops:.2f} IOPS')
    ax2.legend()
    
    # Chart 3: Latency over iterations
    latency_data = [it['latency_mean_ms'] for it in iterations]
    ax3.plot(iterations_data, latency_data, '^-', linewidth=2, markersize=8, color='orange')
    ax3.set_title('Mean Latency Over Iterations', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Latency (ms)')
    ax3.grid(True, alpha=0.3)
    
    # Add average line
    avg_latency = np.mean(latency_data)
    ax3.axhline(y=avg_latency, color='red', linestyle='--', alpha=0.7,
                label=f'Average: {avg_latency:.2f} ms')
    ax3.legend()
    
    # Chart 4: Summary metrics
    metrics = ['Throughput\n(MiB/s)', 'Memory\n(MiB)', 'IOPS', 'Latency\n(ms)']
    values = [
        parsed_data['value'],
        memory_data['value'],
        np.mean(iops_data),
        np.mean(latency_data)
    ]
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    bars = ax4.bar(metrics, values, color=colors, alpha=0.7)
    ax4.set_title('Summary Metrics', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Value')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../../results/benchmark_performance_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_simple_summary():
    """Create a simple summary chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Load data
    parsed_data = load_parsed_results()
    memory_data = load_memory_results()
    
    # Performance vs Memory chart
    categories = ['Performance\n(MiB/s)', 'Memory Usage\n(MiB)']
    values = [parsed_data['value'], memory_data['value']]
    colors = ['#2E86AB', '#A23B72']
    
    bars = ax1.bar(categories, values, color=colors, alpha=0.7)
    ax1.set_title('Performance vs Memory Usage', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Value')
    
    # Add value labels
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Pie chart showing the ratio
    total = parsed_data['value'] + memory_data['value']
    sizes = [parsed_data['value'], memory_data['value']]
    labels = [f'Performance\n({parsed_data["value"]:.2f} MiB/s)', 
              f'Memory\n({memory_data["value"]:.2f} MiB)']
    colors_pie = ['#2E86AB', '#A23B72']
    
    ax2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Performance vs Memory Ratio', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../../results/benchmark_summary.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_iteration_analysis():
    """Create detailed iteration analysis"""
    iterations = load_iteration_data()
    
    if not iterations:
        print("No iteration data found!")
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    iterations_data = [it['iteration'] for it in iterations]
    throughput_data = [it['throughput_mib'] for it in iterations]
    iops_data = [it['iops'] for it in iterations]
    latency_data = [it['latency_mean_ms'] for it in iterations]
    
    # Throughput analysis
    ax1.plot(iterations_data, throughput_data, 'o-', linewidth=2, markersize=8, color='#2E86AB')
    ax1.fill_between(iterations_data, throughput_data, alpha=0.3, color='#2E86AB')
    ax1.set_title('Throughput Analysis', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Throughput (MiB/s)')
    ax1.grid(True, alpha=0.3)
    
    # Add statistics
    mean_throughput = np.mean(throughput_data)
    std_throughput = np.std(throughput_data)
    ax1.axhline(y=mean_throughput, color='red', linestyle='--', alpha=0.7,
                label=f'Mean: {mean_throughput:.2f} ± {std_throughput:.2f}')
    ax1.legend()
    
    # IOPS analysis
    ax2.plot(iterations_data, iops_data, 's-', linewidth=2, markersize=8, color='#A23B72')
    ax2.fill_between(iterations_data, iops_data, alpha=0.3, color='#A23B72')
    ax2.set_title('IOPS Analysis', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('IOPS')
    ax2.grid(True, alpha=0.3)
    
    mean_iops = np.mean(iops_data)
    std_iops = np.std(iops_data)
    ax2.axhline(y=mean_iops, color='red', linestyle='--', alpha=0.7,
                label=f'Mean: {mean_iops:.2f} ± {std_iops:.2f}')
    ax2.legend()
    
    # Latency analysis
    ax3.plot(iterations_data, latency_data, '^-', linewidth=2, markersize=8, color='#F18F01')
    ax3.fill_between(iterations_data, latency_data, alpha=0.3, color='#F18F01')
    ax3.set_title('Latency Analysis', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Latency (ms)')
    ax3.grid(True, alpha=0.3)
    
    mean_latency = np.mean(latency_data)
    std_latency = np.std(latency_data)
    ax3.axhline(y=mean_latency, color='red', linestyle='--', alpha=0.7,
                label=f'Mean: {mean_latency:.2f} ± {std_latency:.2f}')
    ax3.legend()
    
    # Correlation scatter plot
    ax4.scatter(throughput_data, latency_data, s=100, alpha=0.7, color='#C73E1D')
    ax4.set_title('Throughput vs Latency Correlation', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Throughput (MiB/s)')
    ax4.set_ylabel('Latency (ms)')
    ax4.grid(True, alpha=0.3)
    
    # Add correlation coefficient
    correlation = np.corrcoef(throughput_data, latency_data)[0, 1]
    ax4.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
             transform=ax4.transAxes, fontsize=12, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('../../results/benchmark_iteration_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Generating benchmark charts...")
    
    try:
        # Create comprehensive performance chart
        print("Creating comprehensive performance chart...")
        create_performance_chart()
        
        # Create simple summary
        print("Creating simple summary chart...")
        create_simple_summary()
        
        # Create iteration analysis
        print("Creating iteration analysis...")
        create_iteration_analysis()
        
        print("Charts generated successfully!")
        print("Files created in ../../results/")
        print("- benchmark_performance_chart.png")
        print("- benchmark_summary.png") 
        print("- benchmark_iteration_analysis.png")
        
    except Exception as e:
        print(f"Error generating charts: {e}")
        print("Make sure you're running this script from the tools/benchmark-charts directory") 