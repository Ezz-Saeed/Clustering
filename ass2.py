import pandas as pd
import random
import math
import tkinter as tk
from tkinter import filedialog, messagebox


class K_MEANS_CLUSTERING:
    def __init__(self, k):
        self.n_clusters = k

    def load_data(self, file_path, percentage):
        data = pd.read_csv(file_path)
        data.dropna()
        num_rows_to_keep = int(len(data) * (percentage / 100))
        data = data.head(num_rows_to_keep)
        return data

    def initialize_centroids(self, points, num_clusters):
        centroids = random.sample(points, num_clusters)
        return centroids

    def calc_euclidean_distance(self, point1, point2):
        if len(point1) != len(point2):
            raise ValueError("The dimensions of the points must be the same.")
        squared_distances = [(a - b) ** 2 for a, b in zip(point1, point2)]
        distance = math.sqrt(sum(squared_distances))
        return distance

    def assign_points_to_clusters(self, points, centroids):
        cluster_assignments = []

        for point in points:
            distances = [self.calc_euclidean_distance(point, centroid) for centroid in centroids]
            nearest_cluster_index = distances.index(min(distances))
            cluster_assignments.append(nearest_cluster_index)
        return cluster_assignments

    def generate_new_centroids(self, points, clusters, k):
        new_centroids = []
        for i in range(k):
            cluster_points = []
            for j, cluster in enumerate(clusters):
                if cluster == i:
                    cluster_points.append(points[j])
            if cluster_points:
                new_centroid = [sum(coord) / len(cluster_points) for coord in zip(*cluster_points)]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(random.choice(points))
        return new_centroids

    def fit(self, points, k):
        centroids = self.initialize_centroids(points, k)
        clusters = self.assign_points_to_clusters(points, centroids)
        while True:
            new_centroids = self.generate_new_centroids(points, clusters, k)
            new_clusters = self.assign_points_to_clusters(points, new_centroids)
            if new_clusters == clusters:
                break
            centroids = new_centroids
            clusters = new_clusters
        return clusters

    def print_clusters(self, data, clusters):
        output = ""
        unique_clusters = set(clusters)
        for cluster in unique_clusters:
            cluster_indices = [i for i, c in enumerate(clusters) if c == cluster]
            cluster_data = data.iloc[cluster_indices]
            output += f"Cluster {cluster} => Number of films {len(cluster_data)}:\n"
            output += f"{cluster_data[['Movie Name', 'IMDB Rating']]}\n\n"

        outliers = get_outlier_data(data, clusters)
        if not outliers.empty:
            output += "Outlier records:\n"
            output += f"{outliers[['Movie Name', 'IMDB Rating']]}\n"

        return output


def get_data():
    percentage = float(entry_percentage.get())
    k = int(entry_clusters.get())
    file_path = filedialog.askopenfilename()
    return percentage, k, file_path


def get_outlier_data(data, clusters):
    outlier_indices = []
    overall_mean = data['IMDB Rating'].mean()
    overall_std = data['IMDB Rating'].std()
    outliers = data[
        (data['IMDB Rating'] < overall_mean - 2 * overall_std) |
        (data['IMDB Rating'] > overall_mean + 2 * overall_std)
        ]
    outlier_indices.extend(outliers.index.tolist())
    return data.iloc[outlier_indices]



def run_KMeans_clustering():
    percentage, k, file_path = get_data()
    k_means = K_MEANS_CLUSTERING(k)
    data = k_means.load_data(file_path, percentage)
    points = data['IMDB Rating'].values.tolist()
    points = [[point] for point in points]
    clusters = k_means.fit(points, k)
    data['Cluster'] = clusters
    output_text = k_means.print_clusters(data, clusters)
    output_text_widget.delete(1.0, tk.END)
    output_text_widget.insert(tk.END, output_text)




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

button = tk.Button(window, text="Select CSV File", command=run_KMeans_clustering)
button.pack()


output_text_widget = tk.Text(window, height=20, width=80)
output_text_widget.pack()

window.mainloop()
