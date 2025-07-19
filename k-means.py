import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os

# Load the dataset
try:
    df = pd.read_csv('Mall_Customers.csv')
except FileNotFoundError:
    print("Error: 'Mall_Customers.csv' not found. Ensure the file is in the correct directory.")
    exit()
except Exception as e:
    print(f"An error occurred while loading the data: {e}")
    exit()

print("Original DataFrame Head:")
print(df.head())
print("\nDataFrame Info:")
df.info()
print("\nDataFrame Description:")
print(df.describe())

# Select features for clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# Scale the features for K-Means
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine optimal number of clusters using the Elbow Method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Method graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.grid(True)
plt.savefig('elbow_method_plot.png') # Save the plot before showing
print("Elbow Method plot saved as 'elbow_method_plot.png'")
plt.show() # Display the plot
plt.close() # Close the plot to free up memory

print("\nBased on the Elbow Method plot, K=5 is a common choice.")

# Apply K-Means clustering with K=5
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Get and unscale cluster centroids for interpretation
centroids_scaled = kmeans.cluster_centers_
centroids_unscaled = scaler.inverse_transform(centroids_scaled)
centroids_df = pd.DataFrame(centroids_unscaled, columns=['Annual Income (k$)', 'Spending Score (1-100)'])
centroids_df['Cluster'] = range(n_clusters)

print("\nCluster Centroids (Unscaled):")
print(centroids_df)

# Visualize the clusters
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster', data=df,
                palette='viridis', s=100, alpha=0.8, edgecolor='w')
plt.scatter(centroids_unscaled[:, 0], centroids_unscaled[:, 1],
            marker='X', s=300, color='red', label='Centroids', edgecolor='black')
plt.title('Customer Segments based on Annual Income and Spending Score')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.grid(True)
plt.savefig('customer_segments_plot.png') # Save the plot before showing
print("Customer Segments plot saved as 'customer_segments_plot.png'")
plt.show() # Display the plot
plt.close() # Close the plot to free up memory

print("\nCustomer DataFrame with Cluster Assignments:")
print(df.head())

# Analyze characteristics of each cluster
print("\nCharacteristics of each cluster:")
print(df.groupby('Cluster').agg({
    'CustomerID': 'count',
    'Gender': lambda x: x.mode()[0] if not x.empty else 'N/A',
    'Age': 'mean',
    'Annual Income (k$)': 'mean',
    'Spending Score (1-100)': 'mean'
}).rename(columns={'CustomerID': 'Count'}))