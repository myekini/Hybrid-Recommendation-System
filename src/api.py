# src/api.py

from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
from src.models.hybrid import recommend_hybrid

# Load metadata once at startup
merged_df = pd.read_csv("data/processed/merged_data.csv")

app = FastAPI(title="Hybrid Recommendation API")

@app.get("/recommend/{user_id}", response_model=List[dict])
def recommend(user_id: str, top_n: int = 10):
    try:
        recommendations = recommend_hybrid(user_id, top_n=top_n)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found.")

        # Use the actual column names from your merged dataset.
        # Here we use 'video_id', 'Name_y' (video title), 'Description', 'Category', and 'Tags'
        video_info = merged_df[merged_df['video_id'].isin(recommendations)][
            ['video_id', 'Name_y', 'Description', 'Category', 'Tags']
        ]
        
        # Optionally, rename columns for a cleaner API response:
        video_info = video_info.rename(columns={'Name_y': 'title'})
        
        result = video_info.to_dict(orient="records")
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the Hybrid Recommender API"}

@app.get("/health")
def health():
    return {"status": "ok"}
