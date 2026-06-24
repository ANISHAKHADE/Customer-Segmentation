from flask import Flask, request, jsonify,render_template
import joblib
import numpy as np

app = Flask(__name__)

# 1. Load the frozen brains on startup
try:
    scaler = joblib.load('rfm_scaler.joblib')
    kmeans_model = joblib.load('kmeans_model.joblib')
    print("🧠 ML Models loaded successfully into API memory!")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# Exact segment map matching your training script
SEGMENT_MAP = {
    0: 'New/Promising',
    1: 'Champions',
    2: 'At-Risk'
}

# 2. ADD THIS NEW ROUTE RIGHT HERE TO SERVE THE HTML FRONTEND
@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict_customer_segment():
    try:
        # 2. Extract raw features from URL query parameters
        # Example: /predict?recency=5&frequency=14&monetary=12000
        recency = float(request.args.get('recency'))
        frequency = float(request.args.get('frequency'))
        monetary = float(request.args.get('monetary'))
    except (TypeError, ValueError):
        return jsonify({
            'status': 'error',
            'message': 'Missing or invalid parameters. Please provide numeric recency, frequency, and monetary values.'
        }), 400

    # 3. Shape data into a 2D array for Scikit-Learn [[R, F, M]]
    raw_data = np.array([[recency, frequency, monetary]])

    # 4. CRITICAL ML RULE: Use .transform(), NOT .fit_transform()!
    # We want to scale using the exact historical parameters we trained on.
    scaled_data = scaler.transform(raw_data)

    # 5. Predict the cluster number
    predicted_cluster = int(kmeans_model.predict(scaled_data)[0])
    assigned_segment = SEGMENT_MAP[predicted_cluster]

    # 6. Return a clean JSON API response
    return jsonify({
        'status': 'success',
        'input_data': {
            'recency_days': recency,
            'frequency_orders': frequency,
            'total_monetary_spend': monetary
        },
        'ml_output': {
            'cluster_id': predicted_cluster,
            'segment_label': assigned_segment
        }
    })

if __name__ == '__main__':
    # Start local development server
    app.run(debug=True, port=5000)