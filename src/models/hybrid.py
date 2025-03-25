import pickle
import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

def recommend_hybrid(user_id, top_n=10, alpha=0.6):
    """
    Recommend videos for a given user_id using a hybrid of collaborative filtering and content-based methods.
    Falls back to collaborative filtering if content-based features are unavailable.
    """
    # Load trained ALS model and mappings
    with open("data/processed/als_model.pkl", "rb") as f:
        model, mappings = pickle.load(f)
    
    # Load merged data
    merged_df = pd.read_csv("data/processed/merged_data.csv")
    
    # Check if the user exists in our interaction mapping
    if user_id not in mappings["user_id_to_idx"]:
        print(f"User {user_id} not found in training data.")
        return []
    
    user_idx = mappings["user_id_to_idx"][user_id]
    
    # Load TF-IDF matrix; it might be empty if content-based features weren't computed
    tfidf_matrix = load_npz("data/processed/tfidf_matrix.npz")
    
    # --- Collaborative Filtering Component ---
    try:
        # Get recommendations from collaborative filtering using implicit ALS
        # (Here we use the model's recommend function which returns (item_idx, score) tuples)
        cf_recs = model.recommend(user_idx, 
                                  filter_already_liked_items=True, 
                                  N=top_n)
        collab_scores = {mappings["idx_to_video_id"][item_idx]: score for item_idx, score in cf_recs}
    except Exception as e:
        print(f"Error in collaborative filtering: {e}")
        collab_scores = {}
    
    # --- Content-Based Component ---
    # Check if TF-IDF matrix has any features
    if tfidf_matrix.shape[1] > 0:
        # Get indices for videos that the user interacted with
        user_video_indices = merged_df[merged_df['user_id'] == user_id].index
        if len(user_video_indices) > 0:
            # Build a user profile vector as the mean of the TF-IDF vectors of interacted videos
            user_vector = tfidf_matrix[user_video_indices].mean(axis=0)
            # Compute cosine similarity between the user vector and all video vectors
            content_sim = cosine_similarity(user_vector, tfidf_matrix).flatten()
            # Get top indices and their scores
            content_indices = np.argsort(content_sim)[::-1][:top_n]
            content_scores = {merged_df.iloc[i]['video_id']: content_sim[i] for i in content_indices}
        else:
            print(f"No interactions found for user {user_id} for content-based filtering.")
            content_scores = {}
    else:
        print("Content-based features are unavailable. Using collaborative filtering only.")
        content_scores = {}

    # --- Combine the Two Components ---
    # If both components are available, fuse their scores.
    # If content-based is empty, use only collaborative scores.
    combined_scores = {}
    if content_scores:
        all_video_ids = set(collab_scores.keys()).union(content_scores.keys())
        for vid in all_video_ids:
            c_score = collab_scores.get(vid, 0)
            t_score = content_scores.get(vid, 0)
            combined_scores[vid] = alpha * c_score + (1 - alpha) * t_score
    else:
        combined_scores = collab_scores

    # Sort the videos by their combined score in descending order and return top_n video ids.
    top_videos = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [vid for vid, score in top_videos]
