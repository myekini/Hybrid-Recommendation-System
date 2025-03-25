import os
import streamlit as st
import pandas as pd
import requests

# Must be the very first Streamlit command
st.set_page_config(page_title="🎬 Hybrid Recommender", layout="centered")

# Optional: Allow API URL override from sidebar
default_api_url = os.getenv("API_URL", "https://hybrid-recommendation-system-tezda.streamlit.app/")
api_url = st.sidebar.text_input("API URL", value=default_api_url)

st.title("🎬 Personalized Video Recommender")
st.write("Enter a user ID to get smart video suggestions using our hybrid AI model.")

user_id = st.text_input("User ID", placeholder="e.g. 66e9c5755f042a244c705693")
top_n = st.slider("Number of Recommendations", 5, 20, 10)

if st.button("🔍 Get Recommendations") and user_id:
    with st.spinner("Fetching personalized videos..."):
        try:
            request_url = f"{api_url}/recommend/{user_id}?top_n={top_n}"
            response = requests.get(request_url)
            if response.status_code == 200:
                results = response.json()
                if not results:
                    st.warning("No recommendations found for this user.")
                else:
                    st.success(f"Top {top_n} recommendations for {user_id}")
                    for item in results:
                        st.markdown(f"""
                        **🎥 {item.get('title', 'No Title')}**
                        - Category: `{item.get('category', 'N/A')}`
                        - Tags: `{item.get('tags', 'N/A')}`
                        - Description: {item.get('description', '')[:200]}...
                        ---
                        """)
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
