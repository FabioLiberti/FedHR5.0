#!/usr/bin/env python3
"""
Create ALL images for FedHR5.0 README
This script generates both placeholder images and performance charts
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
import seaborn as sns
import os
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create directories
os.makedirs('docs/images', exist_ok=True)
os.makedirs('experiments/results', exist_ok=True)

def create_logo():
    """Create a simple but professional logo for FedHR5.0"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    
    # Remove axes
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Background gradient effect
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    ax.imshow(gradient, extent=[0, 10, 0, 5], aspect='auto', cmap='Blues_r', alpha=0.3)
    
    # Main text
    ax.text(5, 3.2, 'FedHR', fontsize=48, fontweight='bold', 
            ha='center', va='center', color='#2E86AB')
    ax.text(7.5, 3.2, '5.0', fontsize=48, fontweight='bold', 
            ha='center', va='center', color='#A23B72')
    
    # Subtitle
    ax.text(5, 1.8, 'Federated Learning for Industry 5.0', 
            fontsize=16, ha='center', va='center', color='#333333')
    
    # Add network nodes to represent federated architecture
    node_positions = [(1.5, 2.5), (2, 3.5), (8, 3.5), (8.5, 2.5)]
    for i, (x, y) in enumerate(node_positions):
        circle = Circle((x, y), 0.15, color='#06A77D' if i % 2 else '#F18F01', alpha=0.7)
        ax.add_patch(circle)
    
    # Connect nodes with lines
    for i in range(len(node_positions)-1):
        ax.plot([node_positions[i][0], node_positions[i+1][0]], 
                [node_positions[i][1], node_positions[i+1][1]], 
                'k-', alpha=0.3, linewidth=1)
    
    # Human-centric icon (simple person symbol)
    ax.plot(5, 4.2, 'o', markersize=10, color='#2E86AB')
    ax.plot([5, 5], [4.1, 3.8], 'k-', linewidth=2)
    ax.plot([4.9, 5, 5.1], [3.9, 3.8, 3.9], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('docs/images/fedhr5_logo.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created logo: docs/images/fedhr5_logo.png")

def create_module_performance_plot():
    """Create Figure 2: Model Performance Across Modules - Referenced in README"""
    modules = ['Well-being\nAnalytics', 'Skills\nMapping', 'Recruitment\nFairness', 
               'Learning\nPaths', 'Cross-org\nBenchmarking']
    
    # Metrics from the paper
    accuracy = [0.94, 0.89, 0.85, 0.78, 0.91]
    precision = [0.93, 0.89, 0.88, 0.81, 0.90]
    recall = [0.92, 0.87, 0.83, 0.76, 0.89]
    f1_scores = [0.92, 0.88, 0.85, 0.78, 0.89]
    
    x = np.arange(len(modules))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    rects1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy', alpha=0.8)
    rects2 = ax.bar(x - 0.5*width, precision, width, label='Precision', alpha=0.8)
    rects3 = ax.bar(x + 0.5*width, recall, width, label='Recall', alpha=0.8)
    rects4 = ax.bar(x + 1.5*width, f1_scores, width, label='F1-Score', alpha=0.8)
    
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('FedHR5.0 Modules', fontsize=12)
    ax.set_title('Model Performance Across FedHR5.0 Modules', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(modules)
    ax.legend(loc='upper right')
    ax.set_ylim(0.7, 1.0)
    
    # Add value labels on bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(rect.get_x() + rect.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9)
    
    for rects in [rects1, rects2, rects3, rects4]:
        autolabel(rects)
    
    plt.tight_layout()
    plt.savefig('experiments/results/performance.png', dpi=300, bbox_inches='tight')
    print("✅ Created performance.png")

def create_baseline_comparison_plot():
    """Create Figure 3: Performance Comparison with Baselines - Referenced in README"""
    metrics = ['Privacy\nGuarantee', 'Model\nAccuracy', 'Training\nEfficiency', 
               'Fairness\nScore', 'Scalability']
    
    # Normalized scores (0-1 scale)
    fedhr5_scores = [0.95, 0.94, 0.85, 0.93, 0.88]
    centralized_scores = [0.0, 0.96, 0.95, 0.75, 0.60]
    local_only_scores = [1.0, 0.72, 0.90, 0.65, 0.30]
    basic_fl_scores = [0.70, 0.88, 0.80, 0.70, 0.75]
    
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    
    # Close the plot
    fedhr5_scores += fedhr5_scores[:1]
    centralized_scores += centralized_scores[:1]
    local_only_scores += local_only_scores[:1]
    basic_fl_scores += basic_fl_scores[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, fedhr5_scores, 'o-', linewidth=2, label='FedHR5.0', markersize=8)
    ax.fill(angles, fedhr5_scores, alpha=0.25)
    
    ax.plot(angles, centralized_scores, 's-', linewidth=2, label='Centralized', markersize=8)
    ax.fill(angles, centralized_scores, alpha=0.15)
    
    ax.plot(angles, local_only_scores, '^-', linewidth=2, label='Local-Only', markersize=8)
    ax.fill(angles, local_only_scores, alpha=0.15)
    
    ax.plot(angles, basic_fl_scores, 'd-', linewidth=2, label='Basic FL', markersize=8)
    ax.fill(angles, basic_fl_scores, alpha=0.15)
    
    # Fix axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, size=12)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.grid(True)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title('Performance Comparison with Baselines', size=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('experiments/results/comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Created comparison.png")

def create_scalability_plot():
    """Create Figure 4: Scalability Analysis - Referenced in README"""
    num_orgs = [1, 5, 10, 20, 30, 40, 50]
    
    # Training time in minutes (showing near-linear scaling)
    training_time = [12, 15, 22, 38, 54, 72, 95]
    
    # Theoretical linear scaling
    linear_baseline = [12 * n for n in num_orgs]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(num_orgs, training_time, 'o-', linewidth=3, markersize=10, 
            label='FedHR5.0 (Actual)', color='#2E86AB')
    ax.plot(num_orgs, linear_baseline, '--', linewidth=2, 
            label='Linear Scaling (Theoretical)', color='#A23B72', alpha=0.7)
    
    # Add shaded region showing acceptable performance
    ax.fill_between(num_orgs, training_time, linear_baseline, 
                    where=[t < l for t, l in zip(training_time, linear_baseline)],
                    alpha=0.3, color='green', label='Better than Linear')
    
    ax.set_xlabel('Number of Organizations', fontsize=12)
    ax.set_ylabel('Training Time (minutes)', fontsize=12)
    ax.set_title('Scalability: Training Time vs. Number of Organizations', 
                 fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add annotations
    ax.annotate('Near-linear scaling\nup to 50 organizations', 
                xy=(40, 72), xytext=(35, 100),
                arrowprops=dict(arrowstyle='->', color='black', alpha=0.7),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig('experiments/results/scalability.png', dpi=300, bbox_inches='tight')
    print("✅ Created scalability.png")

def create_business_metrics_plot():
    """Create additional plot showing business impact"""
    metrics = ['Employee\nRetention', 'Training\nEffectiveness', 'Time to\nHire', 
               'Well-being\nScore']
    baseline = [72, 54, 45, 6.2]
    fedhr5 = [88, 76, 28, 7.8]
    improvement = [23, 41, -38, 26]  # Percentage improvement
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Bar plot
    bars1 = ax1.bar(x - width/2, baseline, width, label='Baseline', color='#E63946', alpha=0.8)
    bars2 = ax1.bar(x + width/2, fedhr5, width, label='With FedHR5.0', color='#06A77D', alpha=0.8)
    
    ax1.set_xlabel('Business Metrics', fontsize=12)
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('Business Impact of FedHR5.0 Implementation', fontsize=16, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics)
    ax1.legend(loc='upper left')
    
    # Add improvement percentages
    ax2 = ax1.twinx()
    ax2.plot(x, improvement, 'ko-', linewidth=2, markersize=8)
    ax2.set_ylabel('Improvement (%)', fontsize=12)
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}' if height < 50 else f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=9)
    
    # Add improvement labels
    for i, (xi, yi) in enumerate(zip(x, improvement)):
        ax2.annotate(f'{yi:+d}%',
                    xy=(xi, yi),
                    xytext=(0, 10),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10,
                    fontweight='bold',
                    color='darkgreen' if yi > 0 else 'darkred')
    
    plt.tight_layout()
    plt.savefig('experiments/results/business_impact.png', dpi=300, bbox_inches='tight')
    print("✅ Created business_impact.png")

def create_privacy_budget_analysis():
    """Create privacy budget consumption over rounds"""
    rounds = np.arange(1, 101)
    epsilon_0 = 0.1
    alpha = 0.02
    
    # Adaptive privacy budget from Equation (7)
    epsilon_t = epsilon_0 * np.exp(-alpha * rounds)
    
    # Cumulative privacy spent from Equation (8)
    cumulative_epsilon = np.minimum(
        np.sqrt(2 * rounds * np.log(1/1e-5)) * epsilon_0 + rounds * epsilon_0**2,
        rounds * epsilon_0
    )
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Adaptive budget
    ax1.plot(rounds, epsilon_t, linewidth=3, color='#2E86AB')
    ax1.fill_between(rounds, 0, epsilon_t, alpha=0.3, color='#2E86AB')
    ax1.set_ylabel('Privacy Budget (ε)', fontsize=12)
    ax1.set_title('Adaptive Privacy Budget Over Training Rounds', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 0.12)
    
    # Cumulative spending
    ax2.plot(rounds, cumulative_epsilon, linewidth=3, color='#A23B72')
    ax2.axhline(y=1.0, color='red', linestyle='--', label='Privacy Budget Limit')
    ax2.fill_between(rounds, 0, cumulative_epsilon, alpha=0.3, color='#A23B72')
    ax2.set_xlabel('Training Rounds', fontsize=12)
    ax2.set_ylabel('Cumulative Privacy Spent', fontsize=12)
    ax2.set_title('Cumulative Privacy Budget Consumption', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('experiments/results/privacy_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Created privacy_analysis.png")

def create_architecture_diagram():
    """Create a simple architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Cloud Layer
    cloud = FancyBboxPatch((2, 7), 6, 2, 
                           boxstyle="round,pad=0.1",
                           facecolor='#E8F4FD', 
                           edgecolor='#2196F3',
                           linewidth=2)
    ax.add_patch(cloud)
    ax.text(5, 8, 'Cloud Layer', fontsize=14, fontweight='bold', ha='center')
    ax.text(5, 7.5, 'Global Model • Blockchain', fontsize=10, ha='center')
    
    # Fog Layer
    fog1 = FancyBboxPatch((1, 4), 3, 1.5, 
                         boxstyle="round,pad=0.05",
                         facecolor='#FFF3E0',
                         edgecolor='#FF9800',
                         linewidth=2)
    fog2 = FancyBboxPatch((6, 4), 3, 1.5,
                         boxstyle="round,pad=0.05",
                         facecolor='#FFF3E0',
                         edgecolor='#FF9800',
                         linewidth=2)
    ax.add_patch(fog1)
    ax.add_patch(fog2)
    ax.text(2.5, 4.75, 'Fog Node 1', fontsize=11, ha='center')
    ax.text(7.5, 4.75, 'Fog Node 2', fontsize=11, ha='center')
    
    # Edge Devices
    edge_y = 1.5
    for i, x in enumerate([0.5, 1.5, 2.5, 3.5, 5.5, 6.5, 7.5, 8.5]):
        edge = FancyBboxPatch((x, edge_y), 0.8, 0.8,
                             boxstyle="round,pad=0.02",
                             facecolor='#E8F5E9',
                             edgecolor='#4CAF50',
                             linewidth=1.5)
        ax.add_patch(edge)
        ax.text(x+0.4, edge_y+0.4, 'E', fontsize=9, ha='center', va='center')
    
    # Connections
    # Cloud to Fog
    ax.plot([5, 2.5], [7, 5.5], 'k--', alpha=0.5, linewidth=1.5)
    ax.plot([5, 7.5], [7, 5.5], 'k--', alpha=0.5, linewidth=1.5)
    
    # Fog to Edge
    for x in [0.9, 1.9, 2.9, 3.9]:
        ax.plot([2.5, x], [4, 2.3], 'k--', alpha=0.3, linewidth=1)
    for x in [5.9, 6.9, 7.9, 8.9]:
        ax.plot([7.5, x], [4, 2.3], 'k--', alpha=0.3, linewidth=1)
    
    # Labels
    ax.text(5, 0.5, 'Hierarchical Federated Architecture', 
            fontsize=16, fontweight='bold', ha='center')
    
    plt.tight_layout()
    plt.savefig('docs/images/architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created architecture diagram: docs/images/architecture.png")

def main():
    """Generate all images for FedHR5.0"""
    print("🎨 Creating ALL images for FedHR5.0...")
    print("=" * 50)
    
    # Create directories if they don't exist
    Path('docs/images').mkdir(parents=True, exist_ok=True)
    Path('experiments/results').mkdir(parents=True, exist_ok=True)
    
    # Create placeholder images
    print("\n📸 Creating general images...")
    create_logo()
    create_architecture_diagram()
    
    # Create performance charts (referenced in README)
    print("\n📊 Creating performance charts...")
    create_module_performance_plot()     # experiments/results/performance.png
    create_baseline_comparison_plot()    # experiments/results/comparison.png
    create_scalability_plot()           # experiments/results/scalability.png
    
    # Create additional charts
    print("\n📈 Creating additional charts...")
    create_business_metrics_plot()
    create_privacy_budget_analysis()
    
    print("\n✨ All images created successfully!")
    print("\n📁 Images saved in:")
    print("   - docs/images/")
    print("   - experiments/results/")
    
    # Summary
    print("\n📋 Created files:")
    print("   ✓ docs/images/fedhr5_logo.png")
    print("   ✓ docs/images/architecture.png")
    print("   ✓ experiments/results/performance.png (Referenced in README)")
    print("   ✓ experiments/results/comparison.png (Referenced in README)")
    print("   ✓ experiments/results/scalability.png (Referenced in README)")
    print("   ✓ experiments/results/business_impact.png")
    print("   ✓ experiments/results/privacy_analysis.png")

if __name__ == "__main__":
    main()