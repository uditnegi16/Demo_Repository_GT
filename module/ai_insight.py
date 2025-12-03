import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
import json

load_dotenv()

class GeminiInsights:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            st.warning("⚠️ Please add your Gemini API key to .env file")
            api_key = "demo_key"
        
        genai.configure(api_key=api_key)
    
    def get_data_summary_for_ai(self, df):
        """Create comprehensive summary for AI analysis"""
        summary = {
            "dataset_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "memory_size": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
            },
            "columns": list(df.columns),
            "numeric_columns": list(df.select_dtypes(include=['number']).columns),
            "categorical_columns": list(df.select_dtypes(include=['object']).columns),
            "date_columns": [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()],
            "missing_values": int(df.isnull().sum().sum()),
            "sample_data": df.head(3).to_dict(orient='records')
        }
        
        # Add basic statistics for numeric columns
        if summary["numeric_columns"]:
            summary["statistics"] = df[summary["numeric_columns"]].describe().to_dict()
        
        return json.dumps(summary, indent=2)
    
    def analyze_adtech_data(self, df):
        """
        Comprehensive analysis for AdTech data
        """
        try:
            data_summary = self.get_data_summary_for_ai(df)
            
            prompt = f"""
            You are a senior data analyst at an AdTech company. Analyze this dataset and create an executive report.
            
            DATA SUMMARY:
            {data_summary}
            
            TASKS:
            1. **Executive Summary**: Provide a 3-sentence overview of what this data represents
            2. **Key Metrics**: Identify 5 most important metrics/KPIs (with reasoning)
            3. **Trends & Patterns**: Identify 3 key trends or patterns
            4. **Anomalies**: Point out 2 potential issues or anomalies
            5. **Recommendations**: Provide 3 actionable recommendations for campaign optimization
            6. **Insights**: Share 2 surprising or non-obvious insights
            
            FORMAT:
            Use clear headings and bullet points. Be concise but insightful.
            Focus on business impact and actionable insights.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"""
            ## AI Analysis Unavailable
            Error: {str(e)}
            
            **Troubleshooting:**
            1. Check your Gemini API key in .env file
            2. Ensure you have internet connection
            3. Try again in a few moments
            
            **Sample Insights (Based on data structure):**
            - Dataset contains {len(df)} rows and {len(df.columns)} columns
            - Numeric columns: {list(df.select_dtypes(include=['number']).columns)}
            - Consider analyzing conversion rates, click-through rates, and ROI metrics
            """
    
    def generate_report_content(self, df, analysis_text):
        """
        Generate structured report content
        """
        try:
            prompt = f"""
            Based on this analysis:
            {analysis_text}
            
            Create a structured report with:
            
            1. **Cover Page**: Professional title and date
            2. **Table of Contents**
            3. **Introduction**: Brief context
            4. **Methodology**: How analysis was done
            5. **Findings**: Key findings organized
            6. **Recommendations**: Prioritized recommendations
            7. **Conclusion**: Summary and next steps
            
            Format each section for a professional business report.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Report generation failed: {str(e)}"