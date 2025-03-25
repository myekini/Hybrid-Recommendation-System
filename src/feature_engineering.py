# src/feature_engineering.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import networkx as nx
import os


def load_merged_data():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'merged_data.csv')
    return pd.read_csv(path)



from scipy.sparse import csr_matrix

def create_content_tfidf(merged_df: pd.DataFrame):
    """Create TF-IDF vectors from video metadata. If no text is found, return an empty sparse matrix."""
    
    # Define primary and fallback columns
    primary_cols = ['Name_y', 'Description', 'Tags', 'Category']
    fallback_cols = ['VideoTag', 'HashTags']

    # Process primary columns
    for col in primary_cols:
        if col not in merged_df.columns:
            merged_df[col] = ""
        else:
            merged_df[col] = merged_df[col].fillna('').astype(str).str.lower().str.strip()
    
    # Combine primary columns
    merged_df['combined_text'] = (
        merged_df['Name_y'] + ' ' +
        merged_df['Description'] + ' ' +
        merged_df['Tags'] + ' ' +
        merged_df['Category']
    ).str.strip()

    # If primary combined text is empty for all rows, try fallback columns
    if merged_df['combined_text'].eq('').all():
        print("⚠️ Primary text columns are empty. Trying fallback columns:", fallback_cols)
        for col in fallback_cols:
            if col not in merged_df.columns:
                merged_df[col] = ""
            else:
                merged_df[col] = merged_df[col].fillna('').astype(str).str.lower().str.strip()
        merged_df['combined_text'] = (
            merged_df['VideoTag'] + ' ' +
            merged_df['HashTags']
        ).str.strip()

    # Final check: if still no text, skip TF-IDF
    if merged_df['combined_text'].eq('').all():
        print("⚠️ No usable text found for TF-IDF. Skipping content-based feature engineering.")
        n_rows = merged_df.shape[0]
        # Return an empty sparse matrix and empty feature list so downstream code can handle it.
        return csr_matrix((n_rows, 0)), []

    # Optionally, drop rows with completely empty combined text
    merged_df = merged_df[merged_df['combined_text'].str.strip() != '']

    # Build TF-IDF vectors
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(max_features=500)
    tfidf_matrix = tfidf.fit_transform(merged_df['combined_text'])

    print("✅ TF-IDF Matrix Shape:", tfidf_matrix.shape)
    return tfidf_matrix, tfidf.get_feature_names_out()




def create_user_interaction_features(merged_df: pd.DataFrame):
    """Frequency & recency based user interaction features"""
    interaction_stats = merged_df.groupby('user_id').agg({
        'video_id': 'count',
        'timestamp': 'max',
        'watch_time': 'mean'
    }).rename(columns={
        'video_id': 'interaction_count',
        'timestamp': 'last_interaction',
        'watch_time': 'avg_watch_time'
    })

    scaler = MinMaxScaler()
    interaction_stats[['interaction_count', 'avg_watch_time']] = scaler.fit_transform(
        interaction_stats[['interaction_count', 'avg_watch_time']]
    )

    print("✅ Created user interaction features:", interaction_stats.shape)
    return interaction_stats.reset_index()

def create_social_graph_features(followers_df: pd.DataFrame):
    """Use NetworkX to compute centrality"""
    print("Userfollowers columns:", followers_df.columns.tolist())
    G = nx.DiGraph()
    for _, row in followers_df.iterrows():
        # For now, try to use alternative keys if 'follower_id' and 'followee_id' are not present.
        follower = row.get('follower_id', row.get('Follower', None))
        followee = row.get('followee_id', row.get('Followee', None))
        if follower is not None and followee is not None:
            G.add_edge(follower, followee)
    centrality = nx.degree_centrality(G)
    centrality_df = pd.DataFrame.from_dict(centrality, orient='index', columns=['centrality']).reset_index()
    centrality_df.rename(columns={'index': 'user_id'}, inplace=True)
    print("✅ Built social graph & computed centrality:", centrality_df.shape)
    return centrality_df


if __name__ == "__main__":
    from ingestion import load_dataset

    merged_df = load_merged_data()
    tfidf_matrix, tfidf_features = create_content_tfidf(merged_df)

    # Save TF-IDF feature matrix as a sparse .npz file
    from scipy.sparse import save_npz
    save_npz('data/processed/tfidf_matrix.npz', tfidf_matrix)
    print("✅ Saved TF-IDF matrix to data/processed/tfidf_matrix.npz")

    # User interactions
    interaction_features = create_user_interaction_features(merged_df)
    interaction_features.to_csv('data/processed/user_interactions.csv', index=False)

    # Social features
    followers_df = load_dataset("userfollowers.csv")
    social_features = create_social_graph_features(followers_df)
    social_features.to_csv('data/processed/social_features.csv', index=False)
