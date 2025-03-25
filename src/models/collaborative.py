import pandas as pd
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import os
import pickle

MODEL_PATH = "data/processed/als_model.pkl"

def build_interaction_matrix(df: pd.DataFrame):
    """
    Build a sparse user-video interaction matrix based on watch_time.
    Also returns mappings between user/video IDs and their encoded indices.
    """
    # Convert to categorical for efficient integer encoding
    user_ids = df['user_id'].astype('category')
    video_ids = df['video_id'].astype('category')

    # Create index codes
    df['user_idx'] = user_ids.cat.codes
    df['video_idx'] = video_ids.cat.codes

    # Build sparse matrix using watch_time as weight
    sparse_matrix = coo_matrix(
        (df['watch_time'], (df['user_idx'], df['video_idx']))
    ).tocsr()

    mappings = {
        "user_id_to_idx": dict(zip(user_ids, df['user_idx'])),
        "idx_to_user_id": dict(zip(df['user_idx'], user_ids)),
        "video_id_to_idx": dict(zip(video_ids, df['video_idx'])),
        "idx_to_video_id": dict(zip(df['video_idx'], video_ids)),
    }
    return sparse_matrix, mappings

def train_als_model(sparse_matrix):
    """
    Train an Alternating Least Squares (ALS) model using the implicit package.
    """
    model = AlternatingLeastSquares(factors=50, regularization=0.1, iterations=20)
    model.fit(sparse_matrix)
    return model

def save_model(model, mappings):
    """
    Save the trained ALS model and its mapping dictionaries to disk.
    """
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((model, mappings), f)
    print("✅ ALS model trained and saved.")

def run_training():
    """
    Run the complete training pipeline:
    - Load merged interactions,
    - Build the interaction matrix,
    - Train the ALS model,
    - Save the model.
    """
    df = pd.read_csv("data/processed/merged_data.csv")
    sparse_matrix, mappings = build_interaction_matrix(df)
    model = train_als_model(sparse_matrix)
    save_model(model, mappings)

if __name__ == "__main__":
    run_training()
