import pandas as pd
from scipy.spatial import distance
from sklearn.cluster import KMeans
def align_realities(multiverse_df):
    # Select relevant columns for reality alignment
    alignment_df = multiverse_df[['Universe', 'Reality', 'Data']]
    
    # Normalize data for consistent scaling
    alignment_df['Data'] = (alignment_df['Data'] - alignment_df['Data'].min()) / (alignment_df['Data'].max() - alignment_df['Data'].min())
    
    # Define number of reality clusters (hyperparameter tuning possible)
    n_clusters = 5
    
    # Apply K-Means clustering for reality alignment
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(alignment_df[['Data']])
    
    # Add cluster labels to dataframe
    alignment_df['Reality Cluster'] = cluster_labels
    
    # Align realities within clusters
    aligned_realities = alignment_df.groupby(['Universe', 'Reality Cluster'])['Data'].mean().reset_index()
    
    return aligned_realities
def calculate_reality_similarity(aligned_realities):
    # Calculate cosine similarity between reality vectors
    similarity_matrix = distance.cosine(aligned_realities[['Data']].values, aligned_realities[['Data']].values)
    
    # Convert similarity matrix to dataframe
    similarity_df = pd.DataFrame(similarity_matrix, index=aligned_realities['Reality Cluster'], columns=aligned_realities['Reality Cluster'])
    
    return similarity_df

