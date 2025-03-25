# main.py
import os
from src.ingestion import load_all_data
from src.preprocessing import merge_data
from src.feature_engineering import create_content_tfidf, create_user_interaction_features, create_social_graph_features
from src.models.collaborative import run_training
import pandas as pd
from scipy.sparse import save_npz

def run_pipeline():
    # Step 1: Ingest Data
    print("🔁 Loading raw data...")
    data = load_all_data()

    # Step 2: Preprocess Data (merge datasets, clean columns, etc.)
    print("🧼 Preprocessing data...")
    merged_df = merge_data(data)
    print(f"✅ Merged data shape: {merged_df.shape}")

    # Save merged data for later use (API and modeling)
    merged_output_path = os.path.join("data", "processed", "merged_data.csv")
    merged_df.to_csv(merged_output_path, index=False)
    print(f"✅ Saved merged data to {merged_output_path}")

    # Step 3: Feature Engineering
    print("🧬 Running feature engineering...")
    # Create content-based features (TF-IDF)
    try:
        tfidf_matrix, tfidf_features = create_content_tfidf(merged_df)
        save_npz(os.path.join("data", "processed", "tfidf_matrix.npz"), tfidf_matrix)
        print("✅ Saved TF-IDF matrix")
    except Exception as e:
        print(f"⚠️ Skipping TF-IDF creation: {e}")
    
    # Create user interaction features and save them
    interaction_features = create_user_interaction_features(merged_df)
    interaction_features.to_csv(os.path.join("data", "processed", "user_interactions.csv"), index=False)
    print("✅ Saved user interaction features")
    
    # Create social graph features using followers data
    from src.ingestion import load_dataset  # Reuse load_dataset from ingestion
    followers_df = load_dataset("userfollowers.csv")
    social_features = create_social_graph_features(followers_df)
    social_features.to_csv(os.path.join("data", "processed", "social_features.csv"), index=False)
    print("✅ Saved social graph features")
    
    # Step 4: Train Collaborative Filtering Model
    print("🤖 Training collaborative filtering model...")
    run_training()  # This script will load merged_data.csv, build the interaction matrix, train ALS, and save the model.
    print("✅ Pipeline execution completed successfully!")

if __name__ == "__main__":
    run_pipeline()
