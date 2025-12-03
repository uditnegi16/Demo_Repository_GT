import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, df):
        self.df = df
    
    def create_summary_charts(self):
        """Create basic summary charts"""
        charts = {}
        
        # 1. Numeric columns distribution
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            for col in numeric_cols[:4]:  # First 4 numeric columns
                try:
                    fig = px.histogram(self.df, x=col, title=f'Distribution of {col}')
                    charts[f'dist_{col}'] = fig
                except:
                    pass
        
        # 2. Correlation heatmap if enough numeric columns
        if len(numeric_cols) >= 3:
            try:
                corr_matrix = self.df[numeric_cols[:5]].corr()
                fig = px.imshow(corr_matrix, title='Correlation Heatmap')
                charts['correlation'] = fig
            except:
                pass
        
        # 3. Top categories for categorical columns
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) > 0:
            for col in cat_cols[:3]:  # First 3 categorical columns
                try:
                    top_values = self.df[col].value_counts().head(10)
                    fig = px.bar(x=top_values.index, y=top_values.values, 
                                title=f'Top 10 {col}')
                    charts[f'top_{col}'] = fig
                except:
                    pass
        
        return charts
    
    def create_adtech_specific_charts(self):
        """Create charts specific to AdTech data"""
        charts = {}
        
        # Look for common AdTech columns
        column_names = [col.lower() for col in self.df.columns]
        
        # Check for conversion-related columns
        conv_cols = [col for col in self.df.columns if 'conv' in col.lower()]
        click_cols = [col for col in self.df.columns if 'click' in col.lower()]
        cost_cols = [col for col in self.df.columns if 'cost' in col.lower() or 'spend' in col.lower()]
        
        # Conversion rate if possible
        if len(conv_cols) > 0 and len(click_cols) > 0:
            try:
                conv_col = conv_cols[0]
                click_col = click_cols[0]
                self.df['conversion_rate'] = self.df[conv_col] / self.df[click_col] * 100
                fig = px.histogram(self.df, x='conversion_rate', 
                                  title='Conversion Rate Distribution')
                charts['conversion_rate'] = fig
            except:
                pass
        
        # Time series if date column exists
        date_cols = [col for col in self.df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if len(date_cols) > 0 and len(numeric_cols := self.df.select_dtypes(include=['number']).columns) > 0:
            try:
                date_col = date_cols[0]
                metric_col = numeric_cols[0]
                self.df[date_col] = pd.to_datetime(self.df[date_col])
                time_series = self.df.groupby(self.df[date_col].dt.date)[metric_col].sum().reset_index()
                fig = px.line(time_series, x=date_col, y=metric_col, 
                             title=f'{metric_col} Over Time')
                charts['time_series'] = fig
            except:
                pass
        
        return charts