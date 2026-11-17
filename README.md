
# 🎯 E-Commerce Customer Segmentation API

**Live demo:** https://customer-segmentation-plum-phi.vercel.app

## Objective
The goal of this project is to analyze customer purchasing behavior, segment customers into distinct marketing categories using machine learning, and serve those predictions in real time through an API.

Instead of relying on a static CSV file, the project builds a complete pipeline: simulating a relational database, engineering features with SQL, training a K-Means clustering model, and deploying the model with Flask.

## 🛠️ Tech Stack
* **Backend & API:** Python, Flask
* **Database & Data Engineering:** SQLite, SQL (JOIN and aggregation queries for RFM)
* **Machine Learning:** Scikit-Learn (K-Means), Pandas, NumPy
* **Model Serialization:** Joblib
* **Deployment:** Vercel

## 🗂️ Dataset
The data is **synthetic**. `seed_db.py` generates a small e-commerce database (SQLite, `ecommerce.db`) with randomly generated values, so the exact numbers differ each time it is run:

| Table | Rows | Columns |
|-------|------|---------|
| `users` | 200 | user_id, signup_date, country |
| `products` | 6 | product_id, product_name, category, price |
| `transactions` | varies per run | transaction_id, user_id, product_id, transaction_date, quantity |

Each generated customer follows one of three hidden behaviour profiles, which the clustering model is **not** told about:
* **Champion:** 10 to 20 purchases, all within the last 14 days
* **At-risk:** 1 to 5 purchases, 60 to 365 days ago
* **New:** 1 to 3 purchases within the last 30 days

## ⚙️ System Architecture
1. **Data generation (`seed_db.py`):** drops and rebuilds `ecommerce.db` with the three tables above.
2. **Exploration (`eda.py`):** computes RFM features and plots the **Elbow Method** used to choose the number of clusters.
3. **Training (`segmentation.py`):**
   * Runs a SQL query (JOIN + GROUP BY) to compute **RFM** per customer: Recency (days since last order), Frequency (number of orders) and Monetary (total spend = quantity × price).
   * Standardizes the features with `StandardScaler` and trains `KMeans` with 3 clusters.
   * Maps cluster numbers to segment names and saves `rfm_scaler.joblib` and `kmeans_model.joblib`.
4. **API (`app.py`):** a Flask server that loads the saved scaler and model and exposes `/predict`.

## 📊 The Customer Segments
Cluster centres of the deployed model, converted back to original units (trained on 200 customers):

| Segment | Avg recency (days) | Avg frequency (orders) | Avg spend | Suggested action |
|---------|--------------------|------------------------|-----------|------------------|
| 🏆 Champions | 0.6 | 15.1 | 13,580 | Loyalty programs, upsells |
| 🌱 New/Promising | 38.9 | 2.8 | 2,174 | Engagement campaigns, discounts |
| ⚠️ At-Risk | 206.2 | 2.6 | 1,950 | Win-back campaigns |

<img width="1044" height="1096" alt="Screenshot 2026-06-18 201246" src="https://github.com/user-attachments/assets/a8356224-ab2b-41f5-9d42-ef62d2fe253d" />

K-Means numbers its clusters arbitrarily, so the names above were assigned by inspecting these centres: the cluster with the most orders and most recent purchases is "Champions", and the cluster with the longest time since the last purchase is "At-Risk".

**Choosing k = 3:** (calculated via the Elbow method), and three groups map to three clear marketing actions.
<img width="1520" height="1000" alt="Screenshot 2026-06-18 182352" src="https://github.com/user-attachments/assets/a98a6fbb-e8bd-4da0-8326-edc54e3d5605" />
<img width="1986" height="1704" alt="Screenshot 2026-06-18 192222" src="https://github.com/user-attachments/assets/39d864c3-e0a4-4d20-94cf-8a2adb758e08" />

## 🔌 API
**`GET /predict?recency=<days>&frequency=<orders>&monetary=<spend>`**

```
GET /predict?recency=5&frequency=15&monetary=12000
```
```json
{
  "status": "success",
  "input_data": {
    "recency_days": 5.0,
    "frequency_orders": 15.0,
    "total_monetary_spend": 12000.0
  },
  "ml_output": {
    "cluster_id": 1,
    "segment_label": "Champions"
  }
}
```
Missing or non-numeric values return HTTP 400 with an error message.

## 🚀 How to Run Locally
Tested on Python 3.12.

**1. Run the app (the trained model is included)**
```bash
git clone https://github.com/ANISHAKHADE/Customer-Segmentation.git
cd Customer-Segmentation

python -m venv venv
# Windows:      venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 for the web form, or call the API directly: http://127.0.0.1:5000/predict?recency=5&frequency=15&monetary=12000

**2. Rebuild the data and explore (optional)**
```bash
pip install -r requirements-dev.txt   # adds pandas and matplotlib
python seed_db.py                     # creates ecommerce.db
python eda.py                         # Elbow Method plot (see known issues)
python segmentation.py                # trains a new model and saves the .joblib files
```
> **Note:** retraining creates a new random dataset and a new model. K-Means may number its clusters differently, but the segment names in `segmentation.py` and `app.py` are mapped by hand. If you retrain, check the new cluster centres and update the mapping before using the new model.

## 📁 Project Structure
```
Customer-Segmentation/
├── seed_db.py             # builds the synthetic SQLite database
├── eda.py                 # Elbow Method plot
├── segmentation.py        # RFM via SQL, scaling, K-Means, saves the model
├── app.py                 # Flask API + web page
├── templates/index.html   # web form
├── rfm_scaler.joblib      # saved StandardScaler
├── kmeans_model.joblib    # saved K-Means model
├── requirements.txt       # what the deployed app needs
└── requirements-dev.txt   # extra packages for retraining and plots
```

## ⚠️ Limitations and Known Issues
* **The data is synthetic.** The segments were built into the generator, so recovering them shows the pipeline works, not how it would perform on real customers.
* **Hand-written label mapping.** Cluster numbers are mapped to segment names manually. Deriving the names from the cluster centres automatically is planned.
* **`eda.py`:** the Elbow plot works, but the 3D segment plot at the end of the script currently raises a `KeyError` (a missing `Cluster` column). A fix is planned.
* **Input validation:** `/predict` rejects missing and non-numeric values, but does not yet reject `nan` or negative numbers.
* **Only three features** (RFM). Real segmentation would also use product category, discounts, returns and similar signals.
* **Unsupervised, so no accuracy score.** Quality is judged with the Elbow Method and whether the segments make business sense.
