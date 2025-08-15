from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import pymysql
from datetime import datetime
from db.db_config import MYSQL_CONFIG
from analytics import LoanAnalytics
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and analytics
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "loan_approval_pipeline.pkl")
FEATURE_IMPORTANCE_PATH = os.path.join(os.path.dirname(__file__), "model", "feature_importance.json")

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
    
    # Load feature names (this should match the training script)
    feature_names = [
        'no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score',
        'residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value',
        'education_ Not Graduate', 'self_employed_ Yes'
    ]
    
    # Initialize analytics
    analytics = LoanAnalytics(model, feature_names)
    
except Exception as e:
    model_loaded = False
    model_error = str(e)
    analytics = None

def get_db_connection():
    """Create database connection"""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    db_status = "ok" if get_db_connection() else "error"
    return jsonify({
        "status": "ok" if model_loaded else "error",
        "model_loaded": model_loaded,
        "model_path": MODEL_PATH,
        "model_error": None if model_loaded else model_error,
        "database": db_status,
        "analytics_loaded": analytics is not None
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    """Predict loan approval"""
    if not model_loaded:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Parse JSON
        input_data = request.get_json()

        if not input_data:
            return jsonify({"error": "Invalid or empty JSON body"}), 400

        # Validate required fields
        required_fields = [
            'no_of_dependents', 'education', 'self_employed', 'income_annum',
            'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
            'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
        ]
        
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Ensure DataFrame is in the right format for prediction
        df = pd.DataFrame([input_data])  # Wrap in a list for single row

        # Predict
        probability = model.predict_proba(df)[0][1]  # Probability of Approval
        status = "Approved" if probability >= 0.5 else "Rejected"



        # Store prediction in database
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                sql = """
                INSERT INTO applications (
                    no_of_dependents, education, self_employed, income_annum,
                    loan_amount, loan_term, cibil_score, residential_assets_value,
                    commercial_assets_value, luxury_assets_value, bank_asset_value,
                    predicted_probability, predicted_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    input_data['no_of_dependents'], input_data['education'],
                    input_data['self_employed'], input_data['income_annum'],
                    input_data['loan_amount'], input_data['loan_term'],
                    input_data['cibil_score'], input_data['residential_assets_value'],
                    input_data['commercial_assets_value'], input_data['luxury_assets_value'],
                    input_data['bank_asset_value'], probability, status
                ))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as db_error:
            print(f"Database error: {db_error}")
            # Continue without database storage if there's an error

        return jsonify({
            "probability": round(probability, 4),
            "status": status,
            "stored_in_db": conn is not None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/feature-importance", methods=["GET"])
def get_feature_importance():
    """Get feature importance"""
    try:
        if os.path.exists(FEATURE_IMPORTANCE_PATH):
            with open(FEATURE_IMPORTANCE_PATH, 'r') as f:
                feature_importance = json.load(f)
        elif analytics:
            feature_importance = analytics.get_feature_importance()
        else:
            return jsonify({"error": "Feature importance not available"}), 404
        
        return jsonify({"feature_importance": feature_importance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/recommendations", methods=["POST"])
def get_recommendations():
    """Get recommendations to improve loan approval probability"""
    if not analytics:
        return jsonify({"error": "Analytics not available"}), 500

    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "Invalid or empty JSON body"}), 400

        # Get target probability from request, default to 0.8
        target_probability = input_data.get('target_probability', 0.8)

        # Create DataFrame
        df = pd.DataFrame([input_data])

        # Get recommendations
        recommendations = analytics.get_recommendations(df, target_probability)

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/what-if", methods=["POST"])
def what_if_analysis():
    """Perform what-if analysis"""
    if not analytics:
        return jsonify({"error": "Analytics not available"}), 500

    try:
        data = request.get_json()
        input_data = data.get('input_data')
        feature_name = data.get('feature_name')
        min_val = data.get('min_val')
        max_val = data.get('max_val')
        steps = data.get('steps', 10)

        if not all([input_data, feature_name, min_val is not None, max_val is not None]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Create DataFrame
        df = pd.DataFrame([input_data])

        # Perform what-if analysis
        results = analytics.what_if_analysis(df, feature_name, min_val, max_val, steps)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/history", methods=["GET"])
def get_history():
    """Get prediction history"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT * FROM applications 
            ORDER BY created_at DESC 
            LIMIT 50
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"predictions": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analytics/summary", methods=["GET"])
def get_analytics_summary():
    """Get analytics summary including feature importance and model metrics"""
    try:
        summary = {}
        
        # Get feature importance
        if os.path.exists(FEATURE_IMPORTANCE_PATH):
            with open(FEATURE_IMPORTANCE_PATH, 'r') as f:
                summary['feature_importance'] = json.load(f)
        
        # Get model metrics
        eval_metrics_path = os.path.join(os.path.dirname(__file__), "model", "eval_metrics.json")
        if os.path.exists(eval_metrics_path):
            with open(eval_metrics_path, 'r') as f:
                summary['model_metrics'] = json.load(f)
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
