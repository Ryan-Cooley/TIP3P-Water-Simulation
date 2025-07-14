import mdtraj as md
import numpy as np

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
    # Process every 10th frame
    if frame_index % 10 != 0:  # Skip frames that are not a multiple of 10
        continue

    positions = frame.xyz[0][oxygens]  # Positions of all oxygen atoms in this frame
    print(f"Processing frame {frame_index + 1}: {positions.shape[0]} oxygen atoms")

    if positions.shape[0] < 2:
        print(f"Skipping frame {frame_index + 1}: Not enough oxygen atoms.")
        continue

    for i in range(len(positions)):
        current_pos = positions[i]
        # Compute distances from the current oxygen to all others and sort them
        dists = np.linalg.norm(positions - current_pos, axis=1)
        filtered_dists = dists[dists > 0]  # Remove the distance to itself (zero)
        if len(filtered_dists) > 0:
            nearest_distance = np.min(filtered_dists)
            nearest_distances.append(nearest_distance)

if len(nearest_distances) == 0:
    print("Error: No nearest distances were calculated. Check the trajectory data.")
    exit()

# Calculate standard deviation
print("Calculating the standard deviation of nearest distances...")
std_dev = np.std(nearest_distances)
print(f"The standard deviation of nearest distances between oxygen atoms is: {std_dev:.3f} nm")

print("Calculating the mean of nearest distances...")
mean_nearest_distance = np.mean(nearest_distances)
print(f"The mean nearest distance between oxygen atoms is: {mean_nearest_distance:.3f} nm")

# Save the nearest distances to a file
print("Saving nearest distances to file...")
np.savetxt('nearest_distances_waterbox.txt', nearest_distances)
print("Nearest distances saved to 'nearest_distances_waterbox.txt'.")

# Save the standard deviation and mean to a file
print("Saving standard deviation and mean to file...")
with open('stats_box.txt', 'w') as f:
    f.write(f"Standard deviation: {std_dev:.3f} nm\n")
    f.write(f"Mean nearest distance: {mean_nearest_distance:.3f} nm\n")
print("Statistics saved to 'stats_box.txt'.")
