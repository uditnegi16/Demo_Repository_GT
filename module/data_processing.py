import pandas as pd
import streamlit as st
from datetime import datetime
import numpy as np

class DataProcessor:
    def __init__(self, df):
        self.df = df
        self.processed_df = df.copy()
        
    def clean_data(self):
        """Basic data cleaning operations"""
        try:
            # Remove duplicates
            initial_shape = self.processed_df.shape
            self.processed_df = self.processed_df.drop_duplicates()
            duplicates_removed = initial_shape[0] - self.processed_df.shape[0]
            
            # Fill missing numeric values with median
            numeric_cols = self.processed_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.processed_df[col].isnull().sum() > 0:
                    self.processed_df[col].fillna(self.processed_df[col].median(), inplace=True)
            
            # Fill missing categorical values with mode
            cat_cols = self.processed_df.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if self.processed_df[col].isnull().sum() > 0:
                    self.processed_df[col].fillna(self.processed_df[col].mode()[0], inplace=True)
            
            st.success(f"✅ Data cleaned! Removed {duplicates_removed} duplicates")
            return self.processed_df
            
        except Exception as e:
            st.error(f"Error cleaning data: {e}")
            return self.df
    
    def detect_date_columns(self):
        """Detect columns that might be dates"""
        date_columns = []
        for col in self.processed_df.columns:
            # Try to convert to datetime
            try:
                pd.to_datetime(self.processed_df[col], errors='raise')
                date_columns.append(col)
            except:
                pass
        return date_columns
    
    def get_basic_metrics(self):
        """Calculate basic metrics for numerical columns"""
        if self.processed_df is not None:
            numeric_cols = self.processed_df.select_dtypes(include=[np.number]).columns
            
            metrics = {}
            for col in numeric_cols:
                metrics[col] = {
                    'mean': float(self.processed_df[col].mean()),
                    'median': float(self.processed_df[col].median()),
                    'std': float(self.processed_df[col].std()),
                    'min': float(self.processed_df[col].min()),
                    'max': float(self.processed_df[col].max()),
                    'null_count': int(self.processed_df[col].isnull().sum())
                }
            return metrics
        return {}