import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import numpy as np

def get_user_profile(user_id: str, merged_df: pd.DataFrame, tfidf_matrix):
    """
    Construct a user profile vector as the mean of TF-IDF vectors for all videos
    the user has interacted with.
    """
    # Identify rows for the given user
    user_rows = merged_df[merged_df['user_id'] == user_id]
    if user_rows.empty:
        return None
    # Use the indices corresponding to the user interactions
    indices = user_rows.index.tolist()
    # Compute the mean vector from the TF-IDF matrix
    user_vector = tfidf_matrix[indices].mean(axis=0)
    return user_vector

def recommend_content(user_id: str, top_n: int = 10):
    """
    Recommend videos using content-based filtering.
    Returns a list of video_ids.
    """
    # Load merged data and TF-IDF matrix
    merged_df = pd.read_csv("data/processed/merged_data.csv")
    tfidf_matrix = load_npz("data/processed/tfidf_matrix.npz")

    # Build user profile from interacted videos
    user_vector = get_user_profile(user_id, merged_df, tfidf_matrix)
    if user_vector is None:
        print(f"⚠️ No interactions found for user {user_id}.")
        return []

    # Calculate cosine similarity between user vector and all videos
    sim_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    # Get indices of top_n videos (highest similarity scores)
    top_indices = np.argsort(sim_scores)[::-1][:top_n]
    # Retrieve corresponding video_ids from merged data
    top_video_ids = merged_df.iloc[top_indices]['video_id'].tolist()
    return top_video_ids
