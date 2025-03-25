# src/ingestion.py

import pandas as pd
import os

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

def load_dataset(filename: str) -> pd.DataFrame:
    path = os.path.join(RAW_DATA_PATH, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in raw data folder")
    
    df = pd.read_csv(path)
    print(f"✅ Loaded {filename} - shape: {df.shape}")
    return df

def load_all_data():
    interactions = load_dataset('interactions.csv')
    users = load_dataset('userprofiles.csv')
    videos = load_dataset('videos.csv')
    followers = load_dataset('userfollowers.csv')

    return {
        "interactions": interactions,
        "users": users,
        "videos": videos,
        "followers": followers
    }

if __name__ == "__main__":
    data = load_all_data()
    for name, df in data.items():
        print(f"\n📄 {name.upper()} Preview:")
        print(df.head())
