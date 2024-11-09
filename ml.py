# -*- coding: utf-8 -*-
"""Copy of Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E3_O1G32SgD9SSoAz0r857fIcy2BB53b
"""

from google.colab import drive
drive.mount('/content/drive')



import pandas as pd


df = pd.read_csv("/content/sample_data/california_housing_test.csv")

df.head()

!pip install scikit-learn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming df is your DataFrame
# Let's select some numerical features for PCA
X = df[['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value']]

# 1. Center the data (subtract the mean)
X_centered = X - np.mean(X, axis=0)

# 2. Calculate the covariance matrix
covariance_matrix = np.cov(X_centered, rowvar=False)

# 3. Calculate the eigenvalues and eigenvectors of the covariance matrix
eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

# 4. Sort eigenvalues in descending order and select the top k eigenvectors
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Let's choose the top 2 principal components
k = 2
top_k_eigenvectors = eigenvectors[:, :k]

# 5. Project the data onto the new principal component axes
principal_components = np.dot(X_centered, top_k_eigenvectors)


# Plot the principal components
plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of California Housing Data')
plt.show()

import random

def euclidean_distance(point1, point2):
  """Calculates the Euclidean distance between two points."""
  return np.sqrt(np.sum((point1 - point2)**2))

def kmeans(data, k, max_iterations=100):
  """Implements the K-Means clustering algorithm."""

  # 1. Initialize centroids randomly
  centroids = data[random.sample(range(data.shape[0]), k)]

  for _ in range(max_iterations):
    # 2. Assign each data point to the nearest centroid
    clusters = [[] for _ in range(k)]
    for point in data:
      distances = [euclidean_distance(point, centroid) for centroid in centroids]
      cluster_index = np.argmin(distances)
      clusters[cluster_index].append(point)

    # 3. Update centroids based on the mean of the points in each cluster
    new_centroids = []
    for cluster in clusters:
      if cluster:
        new_centroids.append(np.mean(cluster, axis=0))
      else:
        # If a cluster is empty, keep the old centroid
        new_centroids.append(centroids[clusters.index(cluster)])

    # 4. Check for convergence (if centroids haven't changed much)
    if np.allclose(centroids, new_centroids):
      break
    centroids = new_centroids

  return clusters, centroids



def gaussian_mixture_model(data, k, max_iterations=100):
  """Implements the Gaussian Mixture Model (GMM) clustering algorithm."""
  # 1. Initialize parameters (means, covariances, and weights) randomly
  n_samples = data.shape[0]
  means = data[random.sample(range(n_samples), k)]
  covariances = [np.eye(data.shape[1]) for _ in range(k)]
  weights = [1/k] * k


  for _ in range(max_iterations):
      # 2. Calculate the responsibility (probability of each point belonging to each cluster)
      responsibilities = np.zeros((n_samples, k))
      for i in range(n_samples):
          for j in range(k):
              # Use a multivariate Gaussian probability density function
              exponent = -0.5 * np.dot(np.dot((data[i] - means[j]), np.linalg.inv(covariances[j])), (data[i] - means[j]))
              probability = (1 / np.sqrt((2 * np.pi) ** data.shape[1] * np.linalg.det(covariances[j]))) * np.exp(exponent)
              responsibilities[i, j] = weights[j] * probability

      # Normalize responsibilities to make them proper probabilities
      responsibilities /= np.sum(responsibilities, axis=1, keepdims=True)

      # 3. Update parameters (means, covariances, and weights)
      Nk = np.sum(responsibilities, axis=0)
      for j in range(k):
          means[j] = np.sum(responsibilities[:, j].reshape(-1, 1) * data, axis=0) / Nk[j]
          covariances[j] = np.dot((responsibilities[:, j].reshape(-1, 1) * (data - means[j])).T, (data - means[j])) / Nk[j]
          weights[j] = Nk[j] / n_samples


  # Assign each data point to the cluster with the highest responsibility
  cluster_assignments = np.argmax(responsibilities, axis=1)
  clusters = [data[cluster_assignments == i] for i in range(k)]

  return clusters, means


# Example usage:

# Perform K-Means clustering
k = 3 # Number of clusters
clusters_kmeans, centroids_kmeans = kmeans(principal_components, k)


# Perform GMM clustering
clusters_gmm, means_gmm = gaussian_mixture_model(principal_components, k)


# Plot the results (you'll need to adapt this to visualize clusters effectively)
# For example, you could plot the clusters with different colors.

plt.figure(figsize=(8, 6))
for i, cluster in enumerate(clusters_kmeans):
  plt.scatter(cluster[:, 0], cluster[:, 1], label=f'Cluster {i+1}')
plt.scatter([c[0] for c in centroids_kmeans], [c[1] for c in centroids_kmeans], marker='X', s=100, c='black', label='Centroids')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('K-Means Clustering')
plt.legend()
plt.show()


plt.figure(figsize=(8, 6))
for i, cluster in enumerate(clusters_gmm):
  plt.scatter(cluster[:, 0], cluster[:, 1], label=f'Cluster {i+1}')
plt.scatter([m[0] for m in means_gmm], [m[1] for m in means_gmm], marker='X', s=100, c='black', label='Means')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('GMM Clustering')
plt.legend()
plt.show()
