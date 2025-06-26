#!/usr/bin/env python3
"""
Create placeholder images for FedHR5.0 README
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
import os

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

def create_performance_chart():
    """Already created by the previous script"""
    print("⏭️  Performance chart will be created by generate_plots.py")

def create_comparison_radar():
    """Already created by the previous script"""
    print("⏭️  Comparison chart will be created by generate_plots.py")

def create_scalability_plot():
    """Already created by the previous script"""
    print("⏭️  Scalability chart will be created by generate_plots.py")

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

def create_privacy_comparison():
    """Create a privacy comparison visualization"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    methods = ['FedHR5.0', 'Traditional\nCentralized', 'Basic FL', 'Local Only']
    privacy_scores = [95, 10, 70, 100]
    utility_scores = [94, 96, 88, 72]
    colors = ['#2E86AB', '#E63946', '#F77F00', '#06A77D']
    
    x = np.arange(len(methods))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, privacy_scores, width, label='Privacy Score', alpha=0.8)
    bars2 = ax.bar(x + width/2, utility_scores, width, label='Utility Score', alpha=0.8)
    
    # Color bars
    for bar, color in zip(bars1, colors):
        bar.set_color(color)
    for bar, color in zip(bars2, colors):
        bar.set_color(color)
        bar.set_alpha(0.6)
    
    ax.set_xlabel('Method', fontsize=12)
    ax.set_ylabel('Score (%)', fontsize=12)
    ax.set_title('Privacy vs. Utility Trade-off', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend()
    ax.set_ylim(0, 110)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=10)
    
    # Add optimal zone
    ax.axhspan(90, 100, alpha=0.1, color='green', label='Optimal Zone')
    ax.text(0, 95, 'Optimal\nZone', fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('docs/images/privacy_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created privacy comparison: docs/images/privacy_comparison.png")

def create_deployment_timeline():
    """Create a deployment timeline visualization"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Timeline data
    phases = ['Research', 'Development', 'Pilot Testing', 'Italy Deploy', 
              'Germany Deploy', 'Portugal Deploy', 'Evaluation']
    start_times = [0, 2, 4, 6, 7, 8, 12]
    durations = [3, 3, 2, 6, 6, 6, 2]
    colors = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#f4a261', '#f4a261', '#e76f51']
    
    # Create Gantt chart
    for i, (phase, start, duration) in enumerate(zip(phases, start_times, durations)):
        ax.barh(i, duration, left=start, height=0.5, 
                color=colors[i], alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add phase labels
        ax.text(start + duration/2, i, phase, 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Milestones
    milestones = [
        (6, 'First Deployment'),
        (12, 'Full Rollout'),
        (14, 'Paper Submission')
    ]
    
    for time, label in milestones:
        ax.axvline(x=time, color='red', linestyle='--', alpha=0.5)
        ax.text(time, len(phases), label, rotation=45, 
                ha='right', va='bottom', fontsize=9, color='red')
    
    ax.set_ylim(-0.5, len(phases)-0.5)
    ax.set_xlim(0, 15)
    ax.set_xlabel('Timeline (Months)', fontsize=12)
    ax.set_title('FedHR5.0 Development and Deployment Timeline', fontsize=16, fontweight='bold')
    ax.set_yticks([])
    ax.grid(axis='x', alpha=0.3)
    
    # Add current status
    current_month = 14
    ax.axvline(x=current_month, color='green', linewidth=3, alpha=0.7)
    ax.text(current_month, -1, 'Current Status', ha='center', fontsize=10, 
            color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/images/timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created timeline: docs/images/timeline.png")

def main():
    """Generate all placeholder images"""
    print("🎨 Creating placeholder images for FedHR5.0...")
    
    create_logo()
    create_architecture_diagram()
    create_privacy_comparison()
    create_deployment_timeline()
    
    print("\n✨ All placeholder images created!")
    print("\n📝 Note: Run generate_plots.py to create the performance charts")
    print("   that are referenced in the README.")

if __name__ == "__main__":
    main()