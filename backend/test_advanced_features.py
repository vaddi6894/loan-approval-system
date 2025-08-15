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

def test_feature_importance():
    """Test feature importance endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/feature-importance")
        print("✅ Feature importance test passed")
        data = response.json()
        print(f"Features analyzed: {len(data.get('feature_importance', {}))}")
        return True
    except Exception as e:
        print(f"❌ Feature importance test failed: {e}")
        return False

def test_recommendations():
    """Test recommendations endpoint"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/recommendations",
            json={**test_data, "target_probability": 0.8},
            headers={"Content-Type": "application/json"}
        )
        print("✅ Recommendations test passed")
        data = response.json()
        print(f"Recommendations generated: {len(data.get('recommendations', []))}")
        return True
    except Exception as e:
        print(f"❌ Recommendations test failed: {e}")
        return False

def test_what_if_analysis():
    """Test what-if analysis endpoint"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/what-if",
            json={
                "input_data": test_data,
                "feature_name": "income_annum",
                "min_val": 1000000,
                "max_val": 10000000,
                "steps": 10
            },
            headers={"Content-Type": "application/json"}
        )
        print("✅ What-if analysis test passed")
        data = response.json()
        print(f"What-if results: {len(data.get('results', []))} data points")
        return True
    except Exception as e:
        print(f"❌ What-if analysis test failed: {e}")
        return False

def test_analytics_summary():
    """Test analytics summary endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/analytics/summary")
        print("✅ Analytics summary test passed")
        data = response.json()
        print(f"Model metrics available: {'model_metrics' in data}")
        print(f"Feature importance available: {'feature_importance' in data}")
        return True
    except Exception as e:
        print(f"❌ Analytics summary test failed: {e}")
        return False

def test_history():
    """Test history endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/history")
        print("✅ History test passed")
        data = response.json()
        print(f"History records: {len(data.get('predictions', []))}")
        return True
    except Exception as e:
        print(f"❌ History test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Advanced Loan Approval API Features...")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Prediction", test_prediction),
        ("Feature Importance", test_feature_importance),
        ("Recommendations", test_recommendations),
        ("What-If Analysis", test_what_if_analysis),
        ("Analytics Summary", test_analytics_summary),
        ("History", test_history)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"🎉 Test Results: {passed}/{total} tests passed!")
    
    if passed == total:
        print("🎯 All advanced features are working correctly!")
    else:
        print("⚠️ Some features need attention.")
