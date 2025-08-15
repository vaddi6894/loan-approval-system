import requests
import json

# Test data based on the dataset schema
test_data = {
    "no_of_dependents": 2,
    "education": " Graduate",  # Note the leading space
    "self_employed": " No",    # Note the leading space
    "income_annum": 5000000,
    "loan_amount": 15000000,
    "loan_term": 12,
    "cibil_score": 750,
    "residential_assets_value": 5000000,
    "commercial_assets_value": 3000000,
    "luxury_assets_value": 8000000,
    "bank_asset_value": 2000000
}

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/health")
        print("✅ Health check passed")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_prediction():
    """Test prediction endpoint"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print("✅ Prediction test passed")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Loan Approval API...")
    print("=" * 40)
    
    health_ok = test_health()
    print()
    
    if health_ok:
        prediction_ok = test_prediction()
        print()
        
        if prediction_ok:
            print("🎉 All tests passed! The API is working correctly.")
        else:
            print("❌ Prediction test failed.")
    else:
        print("❌ Health check failed. Make sure the Flask app is running.")
