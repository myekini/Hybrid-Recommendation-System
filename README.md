# 🎬 Hybrid Personalized Recommendation System

A production-ready hybrid recommendation system that delivers **personalized short-form video suggestions** to users based on content metadata, user behavior, and social graph signals. Built with a modular architecture, served via a FastAPI REST backend, and optionally demonstrated via a Streamlit web interface.

---

## 🚀 Project Objective

Design and deploy a **hybrid recommendation engine** for immersive e-commerce and social video platforms. The system leverages:

- **Collaborative Filtering** for behavioral similarity
- **Content-Based Filtering** for metadata matching
- **Social Network Analysis** to incorporate follower relationships
- A **REST API** to expose personalized recommendations
- (Optional) **Web UI** for interactive demos

---

## 🧠 System Architecture

The architecture is broken into clearly defined layers, making the system modular, maintainable, and scalable.

![System Architecture](./hybrid_recommendation_architecture.png)

---

## 🗂️ Folder Structure

---

## 📦 Features

✅ Hybrid recommendation engine  
✅ Handles cold-start scenarios (new users/videos)  
✅ Cleanly modularized Python code  
✅ REST API via FastAPI  
✅ Optional Streamlit web app for demo  
✅ Scalable and deployable (AWS-ready)

---

## 📊 Datasets

- `interactions.csv`: user-video interactions (likes, views, watch time)
- `userfollowers.csv`: follower graph (user-user)
- `videos.csv`: video metadata (title, tags, category)
- `userprofiles.csv`: demographics & preferences

---

## 🏗️ Core Modules

### 1. Data Pipeline

- Load & inspect all datasets
- Handle missing/null values
- Merge interactions with user & video metadata

### 2. Feature Engineering

- TF-IDF on text fields
- Recency/frequency weighting
- Social graph metrics (e.g., degree, mutuals)

### 3. Model Building

- **Collaborative Filtering** (ALS via `implicit`)
- **Content-Based** (TF-IDF + cosine similarity)
- **Hybrid Fusion** (weighted score combination with recency rules)

### 4. API Serving (FastAPI)

- `/recommend/{user_id}` – returns ranked recommendations in JSON
- `/video/{video_id}` – fetch video metadata
- `/health` – health check endpoint

---

## ❄️ Cold Start Handling

| Scenario      | Strategy                                                   |
| ------------- | ---------------------------------------------------------- |
| **New User**  | Recommend based on demographic similarity & social network |
| **New Video** | Recommend via content similarity using tags/categories     |

---

## 🌐 Optional Web Interface

- Powered by **Streamlit**
- Enter a `user_id` and see recommended videos with thumbnails and descriptions
- Simple and interactive for demo purposes

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/recommendation-system.git
cd recommendation-system
pip install -r requirements.txt
uvicorn src.api:app --reload
```
