import streamlit as st
import pandas as pd
import requests
import os

# Allow API_URL to be configurable via environment variable or sidebar input
default_api_url = os.getenv("API_URL", "http://localhost:8000")
api_url = st.sidebar.text_input("API URL", value=default_api_url)

st.set_page_config(page_title="🎬 Hybrid Recommender", layout="centered")

st.title("🎬 Personalized Video Recommender")
st.write("Enter a user ID to get smart video suggestions using our hybrid AI model.")

user_id = st.text_input("User ID", placeholder="e.g. 66e9c5755f042a244c705693")
top_n = st.slider("Number of Recommendations", 5, 20, 10)

if st.button("🔍 Get Recommendations") and user_id:
    with st.spinner("Fetching personalized videos..."):
        try:
            # Construct the request URL
            request_url = f"{api_url}/recommend/{user_id}?top_n={top_n}"
            response = requests.get(request_url)
            
            if response.status_code == 200:
                results = response.json()
                if not results:
                    st.warning("No recommendations found for this user.")
                else:
                    st.success(f"Top {top_n} recommendations for user {user_id}:")
                    for item in results:
                        # Fallback to placeholders if keys are missing
                        title = item.get('title', 'No Title')
                        category = item.get('category', 'N/A')
                        tags = item.get('tags', 'N/A')
                        description = item.get('description', 'No Description')
                        st.markdown(f"""
                        **🎥 {title}**
                        - **Category:** `{category}`
                        - **Tags:** `{tags}`
                        - **Description:** {description[:200]}...
                        ---
                        """)
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

# Optional: A button to check API health
if st.sidebar.button("Check API Health"):
    try:
        health_resp = requests.get(f"{api_url}/health")
        if health_resp.status_code == 200:
            st.sidebar.success("API is healthy!")
        else:
            st.sidebar.error("API health check failed.")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
