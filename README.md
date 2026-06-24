# 🎯 E-Commerce Customer Segmentation API

## Objective
The goal of this project is to analyze customer purchasing behavior, segment them into distinct marketing categories using machine learning, and serve those predictions in real-time via a RESTful API. 

Instead of relying on static CSV files, this project features a complete end-to-end pipeline: simulating a relational database, engineering features via SQL, training a K-Means clustering model, and deploying the model using Flask.

## 🛠️ Tech Stack
* **Backend & API:** Python, Flask
* **Database & Data Engineering:** SQLite, SQL (RFM Analysis)
* **Machine Learning:** Scikit-Learn (K-Means Clustering), Pandas, NumPy
* **Model Serialization:** Joblib

## ⚙️ System Architecture
1. **Data Generation (`seed_db.py`):** * Drops and rebuilds a localized SQLite database (`ecommerce.db`).
   * Generates a synthetic e-commerce environment with `users`, `products`, and `transactions` tables.
2. **Machine Learning Pipeline (`segmentation.py`):**
   * Uses complex SQL queries to extract **RFM** metrics (Recency, Frequency, Monetary value) directly from the database.
   * Standardizes the data using `StandardScaler` and determines optimal groupings using the Elbow Method.
   * Trains a `KMeans` algorithm to classify customers into 3 distinct segments.
   * Saves the trained scaler and model as `.joblib` artifacts for production use.
3. **API Deployment (`app.py`):**
   * A Flask web server that loads the pre-trained ML artifacts into memory.
   * Exposes a `/predict` GET endpoint that accepts live user data and returns their predicted customer segment in JSON format.

## 📊 The Customer Segments
Based on the K-Means algorithm, customers are clustered into three actionable business categories:
* 🏆 **Champions:** High spenders, frequent buyers, and recent activity. (Target: Loyalty programs and upsells).
* 🌱 **New/Promising:** Recent buyers with lower frequency. (Target: Engagement campaigns and discounts).
* ⚠️ **At-Risk:** Previous buyers who have not made a transaction in a long time. (Target: Win-back campaigns).

## 🚀 How to Run Locally

**1. Install Dependencies**
```bash
pip install -r requirements.txt