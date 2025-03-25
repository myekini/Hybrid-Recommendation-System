# src/preprocessing.py

import pandas as pd
from ingestion import load_all_data

def clean_interactions(df: pd.DataFrame) -> pd.DataFrame:
    print("📄 Interactions columns:", df.columns.tolist())

    # Rename columns for consistency
    df.rename(columns={'itemId': 'video_id'}, inplace=True)

    # Use eventValue as watch_time
    if 'eventValue' in df.columns:
        df['watch_time'] = df['eventValue'].fillna(1)
    else:
        df['watch_time'] = 1

    # Convert timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    return df



def clean_user_profiles(df: pd.DataFrame) -> pd.DataFrame:
    # Fill missing values for numeric fields
    
    if '_id' in df.columns:
        df.rename(columns={'_id': 'user_id'}, inplace=True)
    if 'age' in df.columns:
        df['age'] = df['age'].fillna(df['age'].median())

    # Safely lowercase only real string-like columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(str).str.lower().str.strip()
            except Exception as e:
                print(f"⚠️ Skipping column '{col}' during string cleaning due to: {e}")

    return df


def clean_videos(df: pd.DataFrame) -> pd.DataFrame:
    print("🎬 Columns in videos.csv:", df.columns.tolist())

    # Rename to standard if needed
    if '_id' in df.columns:
        df.rename(columns={'_id': 'video_id'}, inplace=True)

    # Clean text fields
    for col in ['title', 'description', 'tags', 'category']:
        if col in df.columns:
            df[col] = df[col].fillna('').astype(str).str.lower().str.strip()
    return df


def merge_data(data: dict) -> pd.DataFrame:
    """Merge interactions with user and video metadata"""
    interactions = clean_interactions(data['interactions'])
    users = clean_user_profiles(data['users'])
    videos = clean_videos(data['videos'])

    merged = interactions.merge(users, on='user_id', how='left') \
                         .merge(videos, on='video_id', how='left')

    print(f"✅ Merged Data Shape: {merged.shape}")
    return merged

if __name__ == "__main__":
    data = load_all_data()
    merged_df = merge_data(data)

    # Preview
    print("\n📦 Merged Data Sample:")
    print(merged_df.head())

    # Save for feature engineering
    merged_df.to_csv("data/processed/merged_data.csv", index=False)
    print("✅ Saved merged dataset to data/processed/merged_data.csv")
