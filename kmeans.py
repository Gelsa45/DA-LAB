import math
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

# Function for k-means clustering
def k_means_clustering(data, k, max_iterations=100):
    # Initialize centroids to the first k data points
    centroids = data[:k]

    for iteration in range(max_iterations):
        # Initialize a list to store labels for each data point
        labels = []

        # Assign each point to the closest centroid
        for point in data:
            # Initialize an empty list to store distances to each centroid
            distances = []

            # Calculate the distance from the current point to each centroid
            for i in range(k):
                distance = euclidean_distance(point, centroids[i])
                distances.append(distance)

            # Find the index of the centroid with the smallest distance
            closest_centroid_index = distances.index(min(distances))

            # Append the label for the closest centroid
            labels.append(closest_centroid_index)

        print(f"Iteration {iteration + 1} clusters:")
        for i in range(k):
            cluster_points = [data[j] for j in range(len(data)) if labels[j] == i]
            print(f"Cluster {i + 1}: {cluster_points}")

        # Update centroids
        new_centroids = []
        for i in range(k):
            cluster_points = [data[j] for j in range(len(data)) if labels[j] == i]
            if len(cluster_points) > 0:
                # Initialize a list to store the sum of each dimension
                dimension_sums = [0] * len(data[0])  # Create a list of zeros for each dimension
    
                # Loop through each point in the cluster and sum the dimensions
                for point in cluster_points:
                    # Use zip to sum up the dimensions for all points in one go
                    dimension_sums = [sum(x) for x in zip(dimension_sums, point)]
        
                # Calculate the new centroid by dividing the sums by the number of points
                new_centroid = [dimension_sum / len(cluster_points) for dimension_sum in dimension_sums]
                
                # Append the new centroid to the list of new centroids
                new_centroids.append(new_centroid)

            else:
                new_centroids.append(centroids[i])  # Keep the old centroid if no points are assigned

        # Check for convergence
        if new_centroids == centroids:
            break

        centroids = new_centroids

    return labels, centroids

# Function to plot the clusters
def plot_clusters(data, labels, centroids):
    plt.figure(figsize=(8, 6))

    for i in range(max(labels) + 1):
        cluster_points = [data[j] for j in range(len(data)) if labels[j] == i]
        cluster_points = list(zip(*cluster_points))  # Transpose for plotting
        plt.scatter(cluster_points[0], cluster_points[1], label=f'Cluster {i + 1}')

    centroids_x, centroids_y = zip(*centroids)
    plt.scatter(centroids_x, centroids_y, color='black', marker='.', s=100, label='Centroids')

    plt.title('KMEANS CLUSTERING')
    plt.xlabel('A')
    plt.ylabel('B')
    plt.legend()
    plt.grid()
    plt.show()

# Load data from CSV file
csv_file = "kmeans.csv"  
df = pd.read_csv(csv_file)

# Convert data to a list of points
data = df.values.tolist()

# Get the number of clusters from user input
k = int(input("Enter the number of clusters (k): "))

# Perform k-means clustering
labels, centroids = k_means_clustering(data, k)

# Display the final clusters
print("\nFinal clusters:")
for i in range(k):
    cluster_points = [data[j] for j in range(len(data)) if labels[j] == i]
    print(f"Cluster {i + 1}: {cluster_points}")

# Display the final centroids
print("\nFinal centroids:")
print(centroids)

# Plot the clusters
plot_clusters(data, labels, centroids)
