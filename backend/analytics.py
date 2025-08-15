import numpy as np
import pandas as pd
import json
import os
from sklearn.ensemble import RandomForestClassifier

class LoanAnalytics:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        
    def get_feature_importance(self):
        """Get feature importance from the model"""
        if hasattr(self.model.named_steps['classifier'], 'feature_importances_'):
            importance = self.model.named_steps['classifier'].feature_importances_
            return dict(zip(self.feature_names, importance.tolist()))
        return {}
    

    
    def get_recommendations(self, input_data, target_probability=0.8):
        """Get recommendations to improve loan approval probability"""
        recommendations = []
        
        # Get current prediction
        current_prob = self.model.predict_proba(input_data)[0][1]
        
        if current_prob >= target_probability:
            recommendations.append({
                "type": "success",
                "message": f"Current probability ({current_prob:.2%}) already meets target ({target_probability:.2%})"
            })
            return recommendations
        
        # Try different strategies
        original_data = input_data.copy()
        
        # Strategy 1: Increase income
        income_increase = self._find_income_increase(input_data, target_probability)
        if income_increase:
            recommendations.append({
                "type": "income",
                "message": f"Increase annual income by ₹{income_increase:,.0f}",
                "current": float(input_data['income_annum'].iloc[0]),
                "suggested": float(input_data['income_annum'].iloc[0] + income_increase),
                "impact": "High"
            })
        
        # Strategy 2: Improve CIBIL score
        cibil_improvement = self._find_cibil_improvement(input_data, target_probability)
        if cibil_improvement:
            recommendations.append({
                "type": "cibil",
                "message": f"Improve CIBIL score by {cibil_improvement} points",
                "current": int(input_data['cibil_score'].iloc[0]),
                "suggested": int(input_data['cibil_score'].iloc[0] + cibil_improvement),
                "impact": "High"
            })
        
        # Strategy 3: Reduce loan amount
        loan_reduction = self._find_loan_reduction(input_data, target_probability)
        if loan_reduction:
            recommendations.append({
                "type": "loan_amount",
                "message": f"Reduce loan amount by ₹{loan_reduction:,.0f}",
                "current": float(input_data['loan_amount'].iloc[0]),
                "suggested": float(input_data['loan_amount'].iloc[0] - loan_reduction),
                "impact": "Medium"
            })
        
        # Strategy 4: Adjust loan term
        optimal_term = self._find_optimal_term(input_data, target_probability)
        if optimal_term and optimal_term != input_data['loan_term'].iloc[0]:
            recommendations.append({
                "type": "loan_term",
                "message": f"Change loan term to {optimal_term} months",
                "current": int(input_data['loan_term'].iloc[0]),
                "suggested": optimal_term,
                "impact": "Medium"
            })
        
        return recommendations
    
    def _find_income_increase(self, input_data, target_probability, max_increase=5000000):
        """Find minimum income increase needed"""
        original_income = input_data['income_annum'].iloc[0]
        
        for increase in range(100000, max_increase, 100000):
            test_data = input_data.copy()
            test_data['income_annum'] = original_income + increase
            prob = self.model.predict_proba(test_data)[0][1]
            
            if prob >= target_probability:
                return increase
        
        return None
    
    def _find_cibil_improvement(self, input_data, target_probability, max_improvement=200):
        """Find minimum CIBIL score improvement needed"""
        original_cibil = input_data['cibil_score'].iloc[0]
        
        for improvement in range(10, max_improvement, 10):
            test_data = input_data.copy()
            test_data['cibil_score'] = min(900, original_cibil + improvement)
            prob = self.model.predict_proba(test_data)[0][1]
            
            if prob >= target_probability:
                return improvement
        
        return None
    
    def _find_loan_reduction(self, input_data, target_probability, max_reduction=10000000):
        """Find minimum loan amount reduction needed"""
        original_amount = input_data['loan_amount'].iloc[0]
        
        for reduction in range(100000, max_reduction, 100000):
            test_data = input_data.copy()
            test_data['loan_amount'] = max(100000, original_amount - reduction)
            prob = self.model.predict_proba(test_data)[0][1]
            
            if prob >= target_probability:
                return reduction
        
        return None
    
    def _find_optimal_term(self, input_data, target_probability):
        """Find optimal loan term"""
        original_term = input_data['loan_term'].iloc[0]
        best_term = original_term
        best_prob = self.model.predict_proba(input_data)[0][1]
        
        for term in range(2, 61):  # 2 to 60 months
            test_data = input_data.copy()
            test_data['loan_term'] = term
            prob = self.model.predict_proba(test_data)[0][1]
            
            if prob > best_prob:
                best_prob = prob
                best_term = term
        
        return best_term if best_prob >= target_probability else None
    
    def what_if_analysis(self, input_data, feature_name, min_val, max_val, steps=10):
        """Perform what-if analysis for a specific feature"""
        results = []
        original_value = input_data[feature_name].iloc[0]
        
        for i in range(steps + 1):
            test_value = min_val + (max_val - min_val) * i / steps
            test_data = input_data.copy()
            test_data[feature_name] = test_value
            
            prob = self.model.predict_proba(test_data)[0][1]
            results.append({
                "value": float(test_value),
                "probability": float(prob),
                "status": "Approved" if prob >= 0.5 else "Rejected"
            })
        
        return {
            "feature": feature_name,
            "original_value": float(original_value),
            "results": results
        }
