#!/usr/bin/env python3
"""
Advanced Loan Approval Prediction System - Startup Script
This script helps you start the application with all advanced features.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import pandas
        import sklearn
        import joblib
        import shap
        import matplotlib
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r backend/requirements.txt")
        return False

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Store original directory
    original_dir = Path.cwd()
    
    try:
        # Change to backend directory and start server
        os.chdir(backend_dir)
        
        # Start the Flask app
        subprocess.Popen([sys.executable, "app.py"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        # Return to original directory
        os.chdir(original_dir)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:5000/api/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ Backend server is running on http://127.0.0.1:5000")
                print(f"   - Model loaded: {health_data.get('model_loaded', False)}")
                print(f"   - Analytics loaded: {health_data.get('analytics_loaded', False)}")
                print(f"   - Database: {health_data.get('database', 'unknown')}")
                return True
            else:
                print("❌ Backend server failed to start properly")
                return False
        except requests.exceptions.RequestException:
            print("❌ Backend server is not responding")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        # Return to original directory on error
        os.chdir(original_dir)
        return False

def start_frontend():
    """Start the frontend web interface"""
    print("🌐 Starting frontend web interface...")
    
    # Get absolute path to frontend file
    current_dir = Path.cwd()
    frontend_file = current_dir / "frontend" / "index.html"
    
    print(f"Looking for frontend file at: {frontend_file}")
    
    if not frontend_file.exists():
        print(f"❌ Frontend file not found at {frontend_file}")
        return False
    
    try:
        # Open the frontend in default browser
        webbrowser.open(frontend_file.as_uri())
        print("✅ Frontend opened in web browser")
        return True
    except Exception as e:
        print(f"❌ Failed to open frontend: {e}")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("🏦 Advanced Loan Approval Prediction System")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print()
    
    # Start backend
    if not start_backend():
        print("\n❌ Failed to start backend. Please check the error messages above.")
        return
    
    print()
    
    # Start frontend
    if not start_frontend():
        print("\n❌ Failed to start frontend. Please check the error messages above.")
        return
    
    print()
    print("🎉 Application started successfully!")
    print()
    print("📋 Available Features:")
    print("1. 🧮 Loan Prediction - Instant loan approval predictions")
    print("2. 📊 Probability Breakdown - Visual breakdown of factors")
    print("3. 💡 Explainability (SHAP) - Understand model decisions")
    print("4. 🔄 What-If Analysis - Explore different scenarios")
    print("5. 🎯 Smart Recommendations - Get improvement suggestions")
    print("6. 📈 Analytics Dashboard - Model performance insights")
    print("7. 📚 Prediction History - View past predictions")
    print()
    print("🚀 Instructions:")
    print("1. The backend API is running on http://127.0.0.1:5000")
    print("2. The frontend should have opened in your web browser")
    print("3. Use the side navigation to explore different features")
    print("4. Start with 'Loan Prediction' to make your first prediction")
    print("5. Then explore other features to understand the results")
    print()
    print("🛑 To stop the application, press Ctrl+C in the terminal where the backend is running")
    print("=" * 60)

if __name__ == "__main__":
    main()
