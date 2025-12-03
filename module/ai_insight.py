import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiInsights:
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.warning("⚠️ GEMINI_API_KEY not found. Using demo mode.")
            api_key = "demo_key"  # Placeholder for now
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def analyze_data_summary(self, df):
        """
        Use Gemini to generate data summary
        
        Args:
            df: pandas DataFrame
        
        Returns:
            String with AI-generated insights
        """
        try:
            # Create a text summary of the data
            summary_text = f"""
            Dataset Summary:
            - Shape: {df.shape}
            - Columns: {list(df.columns)}
            - Numeric columns: {list(df.select_dtypes(include=['number']).columns)}
            - Categorical columns: {list(df.select_dtypes(include=['object']).columns)}
            - Missing values: {df.isnull().sum().sum()}
            
            First 3 rows:
            {df.head(3).to_string()}
            """
            
            prompt = f"""
            You are a data analyst at an AdTech company. Analyze this dataset and provide key insights:
            
            {summary_text}
            
            Please provide:
            1. 3 most important observations about this data
            2. 2 potential business insights
            3. 1 recommendation for further analysis
            
            Keep it concise and business-focused.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"⚠️ AI Analysis Error: {str(e)}\n\nPlease check your API key in .env file"
    
    def generate_executive_summary(self, metrics_dict):
        """
        Generate executive summary using Gemini
        
        Args:
            metrics_dict: Dictionary of key metrics
        
        Returns:
            Executive summary text
        """
        try:
            prompt = f"""
            Create an executive summary for an AdTech performance report based on these metrics:
            
            {metrics_dict}
            
            Include:
            1. Overall performance assessment
            2. Key highlights
            3. Areas for improvement
            4. Recommendations
            
            Format as a professional business summary.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Executive summary generation failed: {str(e)}"