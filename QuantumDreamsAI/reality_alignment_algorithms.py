import pandas as pd
from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity # Import for pairwise similarity
import warnings # To handle potential SettingWithCopyWarning
def align_realities(multiverse_df):
    # Select relevant columns for reality alignment
    alignment_df = multiverse_df[['Universe', 'Reality', 'Data']].copy() # Create a copy to avoid SettingWithCopyWarning
    
    # Normalize data for consistent scaling
    alignment_df.loc[:, 'Data'] = (alignment_df['Data'] - alignment_df['Data'].min()) / (alignment_df['Data'].max() - alignment_df['Data'].min())
    
    # Define number of reality clusters (hyperparameter tuning possible)
    n_clusters = 5
    
    # Apply K-Means clustering for reality alignment
    # Set n_jobs=-1 to use all available CPU cores for potentially faster clustering
    # Removed n_jobs=-1 for compatibility with older scikit-learn versions
    # Ensure n_clusters is not more than the number of samples if the dataset is small
    if len(alignment_df[['Data']]) < n_clusters:
        warnings.warn(f"Number of samples ({len(alignment_df[['Data']])}) is less than n_clusters ({n_clusters}). Setting n_clusters to number of samples.")
        n_clusters = len(alignment_df[['Data']])
    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    cluster_labels = kmeans.fit_predict(alignment_df[['Data']])
    
    # Add cluster labels to dataframe
    alignment_df['Reality Cluster'] = cluster_labels
    
    # Align realities within clusters
    aligned_realities = alignment_df.groupby(['Universe', 'Reality Cluster'])['Data'].mean().reset_index()
    
    return aligned_realities
def calculate_reality_similarity(aligned_realities):
    """
    Calculates the pairwise cosine similarity between the average 'Data'
    values of the aligned reality clusters.
    """
    # Pivot the data to have clusters as rows/columns if needed for interpretation,
    # but cosine_similarity works directly on the feature array.
    # Ensure 'Data' is shaped correctly (N_samples, N_features=1)
    data_vectors = aligned_realities[['Data']].values
    
    # Calculate pairwise cosine similarity matrix
    similarity_matrix = cosine_similarity(data_vectors)
    
    # Convert similarity matrix to dataframe
    # Use unique identifiers for index/columns if available, e.g., Reality Cluster IDs
    # Assuming Reality Cluster is unique per row after groupby
    cluster_ids = aligned_realities['Reality Cluster'].unique() # Or use index if appropriate
    similarity_df = pd.DataFrame(similarity_matrix, index=cluster_ids, columns=cluster_ids)
    return similarity_df
