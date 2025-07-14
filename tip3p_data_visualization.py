import numpy as np
import matplotlib.pyplot as plt

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5

# Load nearest distances from the .txt file
nearest_distances = np.loadtxt('nearest_distances_waterbox.txt')

# Create a more professional histogram
fig, ax = plt.subplots(figsize=(12, 8))

# Plot histogram with better styling
n, bins, patches = ax.hist(nearest_distances, bins=50, color='#27AE60', alpha=0.7, 
                           edgecolor='#1a5f3a', linewidth=1.2, density=True)

# Add a vertical line for the mean
mean_distance = np.mean(nearest_distances)
ax.axvline(mean_distance, color='#E74C3C', linestyle='--', linewidth=2, 
           label=f'Mean: {mean_distance:.3f} nm')

# Add a vertical line for the median
median_distance = np.median(nearest_distances)
ax.axvline(median_distance, color='#F39C12', linestyle='--', linewidth=2, 
           label=f'Median: {median_distance:.3f} nm')

# Customize the plot
ax.set_title('Distribution of Nearest Distances Between Water Molecule Oxygens\n(TIP3P Water Box Simulation)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Nearest Distance (nm)', fontsize=14, fontweight='bold')
ax.set_ylabel('Density', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=12)

# Set x-axis limits for better focus
ax.set_xlim(0.225, 0.35)

# Add statistics text box
stats_text = f'Mean: {mean_distance:.3f} nm\nStd Dev: {np.std(nearest_distances):.3f} nm\nCount: {len(nearest_distances)}'
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Adjust layout and save
plt.tight_layout()
plt.savefig('tip3p/nearest_distances_histogram_waterbox.png', dpi=300, bbox_inches='tight')
plt.show()

print("Enhanced histogram saved as 'tip3p/nearest_distances_histogram_waterbox.png'")