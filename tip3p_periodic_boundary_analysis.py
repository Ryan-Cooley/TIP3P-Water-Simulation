import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt

print("Loading trajectory...")
trajectory = md.load('trajectory1.dcd', top='waterbox1.prmtop')  # Adjust filenames

# Check if trajectory loaded correctly
if trajectory is None or len(trajectory) == 0:
    print("Error: Failed to load trajectory or the trajectory is empty.")
    exit()

print("Selecting oxygen atoms...")
oxygens = trajectory.topology.select('name O')
print(f"Number of oxygen atoms found: {len(oxygens)}")

if len(oxygens) == 0:
    print("No oxygen atoms found. Check your topology selections.")
    exit()

print("Finding nearest oxygen atoms in every 10th frame...")
nearest_distances = []
for frame_index, frame in enumerate(trajectory):
    if frame_index % 1000 != 0:  # Process every 10th frame
        continue
    
    print(f"Processing frame {frame_index + 1}...")

    # Compute distances using PBC, 0.5 nm as the cutoff for neighbors (adjust as necessary)
    pairs = md.compute_neighbors(frame, cutoff=0.5, query_indices=oxygens, periodic=True)
    for i, neighbors in enumerate(pairs):
        if len(neighbors) > 0:
            distances = md.compute_distances(frame, [(oxygens[i], n) for n in neighbors], periodic=True)
            nearest_distance = np.min(distances)
            nearest_distances.append(nearest_distance)
            print(f"Frame {frame_index + 1}, oxygen {i + 1}: Nearest distance = {nearest_distance:.3f} nm")

if len(nearest_distances) == 0:
    print("Error: No nearest distances were calculated. Check the trajectory data and PBC settings.")
    exit()


print("Calculating the mean of nearest distances...")
mean_nearest_distance = np.mean(nearest_distances)
print(f"The mean nearest distance between oxygen atoms is: {mean_nearest_distance:.3f} nm")

# find standard deviation of nearest_distances and print
std_nearest_distance = np.std(nearest_distances)
print(f"The standard deviation of nearest distances between oxygen atoms is: {std_nearest_distance:.3f} nm")

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(nearest_distances, bins=30, color='blue', alpha=0.7)
plt.title('Histogram of Nearest Distances Between Water Molecule Oxygens (with PBC)')
plt.xlabel('Nearest Distance (nm)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('nearest_distances_histogram_waterbox_pbc.png')
print("Plot saved as 'nearest_distances_histogram_waterbox_pbc.png'.")