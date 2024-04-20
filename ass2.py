import pandas as pd
import random
import math
import tkinter as tk
from tkinter import filedialog, messagebox


# Read the input file and extract the required percentage of data
def read_data(file_path, percentage):
    data = pd.read_csv(file_path)
    num_rows = int(len(data) * (percentage / 100))
    return data.head(num_rows)


# Calculate Euclidean distance between two data points
import math


def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    if len(point1) != len(point2):
        raise ValueError("The dimensions of the points must be the same.")

    squared_distances = [(a - b) ** 2 for a, b in zip(point1, point2)]
    distance = math.sqrt(sum(squared_distances))
    return distance


# Initialize random centroids
def initialize_centroids(data, k):
    centroids = []
    for _ in range(k):
        centroid = [random.uniform(0, 10)]  # Assuming IMDB rating values range from 0 to 10
        centroids.append(centroid)
    return centroids


# Assign data points to the nearest centroid
def assign_clusters(data, centroids):
    clusters = []
    for point in data:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        cluster = min(range(len(distances)), key=distances.__getitem__)
        clusters.append(cluster)
    return clusters


# Update centroids based on the mean of the assigned data points
def update_centroids(data, clusters, k):
    new_centroids = []
    for i in range(k):
        cluster_points = [data[j] for j in range(len(data)) if clusters[j] == i]
        if cluster_points:
            new_centroid = [sum(coord) / len(cluster_points) for coord in zip(*cluster_points)]
            new_centroids.append(new_centroid)
        else:
            new_centroids.append(random.choice(data))  # Reinitialize empty clusters randomly
    return new_centroids


# Perform k-means clustering
def perform_clustering(data, k):
    centroids = initialize_centroids(data, k)
    clusters = assign_clusters(data, centroids)

    while True:
        new_centroids = update_centroids(data, clusters, k)
        new_clusters = assign_clusters(data, new_centroids)
        if new_clusters == clusters:
            break
        centroids = new_centroids
        clusters = new_clusters

    return clusters


# Identify outlier records based on cluster size
def identify_outliers(data, clusters):
    cluster_counts = [clusters.count(i) for i in range(max(clusters) + 1)]
    cluster_mean = sum(cluster_counts) / len(cluster_counts)
    outlier_clusters = [i for i, count in enumerate(cluster_counts) if count < cluster_mean]
    outliers = data[data['Cluster'].isin(outlier_clusters)]
    return outliers


# Print the content of each cluster and outlier records
def print_clusters(data, clusters):
    output = ""
    unique_clusters = set(clusters)
    for cluster in unique_clusters:
        cluster_indices = [i for i, c in enumerate(clusters) if c == cluster]
        cluster_data = data.iloc[cluster_indices]
        output += f"Cluster {cluster}:\n"
        output += f"{cluster_data[['Movie Name', 'IMDB Rating']]}\n\n"

    outliers = identify_outliers(data, clusters)
    if not outliers.empty:
        output += "Outlier records:\n"
        output += f"{outliers[['Movie Name', 'IMDB Rating']]}\n"

    return output


# Callback function for the "Run Analysis" button
def run_analysis():
    percentage = float(entry_percentage.get())
    k = int(entry_clusters.get())

    file_path = filedialog.askopenfilename()
    if file_path:
        data = read_data(file_path, percentage)
        points = data['IMDB Rating'].values.tolist()
        # Convert points to list of lists
        points = [[point] for point in points]
        clusters = perform_clustering(points, k)
        data['Cluster'] = clusters
        output_text = print_clusters(data, clusters)
        output_text_widget.delete(1.0, tk.END)
        output_text_widget.insert(tk.END, output_text)


# Create the GUI
window = tk.Tk()
window.title("K-means Clustering")
window.geometry("600x400")

label_percentage = tk.Label(window, text="Enter the percentage of data to read:")
label_percentage.pack()

entry_percentage = tk.Entry(window)
entry_percentage.pack()

label_clusters = tk.Label(window, text="Enter the number of clusters (k):")
label_clusters.pack()

entry_clusters = tk.Entry(window)
entry_clusters.pack()

button = tk.Button(window, text="Select CSV File", command=run_analysis)
button.pack()

output_text_widget = tk.Text(window, height=20, width=80)
output_text_widget.pack()

window.mainloop()
