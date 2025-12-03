import pandas as pd
import streamlit as st
import io
from sqlalchemy import create_engine
import os

class DataIngestor:
    def __init__(self):
        self.data = None
        self.data_info = {}
        
    def ingest_csv(self, uploaded_file):
        """Handle CSV file upload"""
        try:
            if uploaded_file.name.endswith('.csv'):
                # Read with pandas
                self.data = pd.read_csv(uploaded_file)
                self._update_data_info()
                st.success(f"✅ CSV loaded successfully! Shape: {self.data.shape}")
                return self.data
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
            return None
    
    def ingest_excel(self, uploaded_file):
        """Handle Excel file upload"""
        try:
            self.data = pd.read_excel(uploaded_file)
            self._update_data_info()
            st.success(f"✅ Excel loaded successfully! Shape: {self.data.shape}")
            return self.data
        except Exception as e:
            st.error(f"Error loading Excel: {e}")
            return None
    
    def ingest_sql(self, connection_string, query):
        """Connect to SQL database and execute query"""
        try:
            engine = create_engine(connection_string)
            self.data = pd.read_sql_query(query, engine)
            self._update_data_info()
            st.success(f"✅ SQL data loaded! Shape: {self.data.shape}")
            return self.data
        except Exception as e:
            st.error(f"Error connecting to SQL: {e}")
            return None
    
    def _update_data_info(self):
        """Update data information dictionary"""
        if self.data is not None:
            buffer = io.StringIO()
            self.data.info(buf=buffer)
            
            self.data_info = {
                'shape': self.data.shape,
                'columns': list(self.data.columns),
                'dtypes': self.data.dtypes.astype(str).to_dict(),
                'info': buffer.getvalue(),
                'missing_values': self.data.isnull().sum().to_dict(),
                'memory_usage': self.data.memory_usage(deep=True).sum() / 1024**2  # MB
            }
    
    def get_data_sample(self, n_rows=5):
        """Return sample of data"""
        if self.data is not None:
            return self.data.head(n_rows)
        return None
    
    def get_data_info(self):
        """Get basic info about the data"""
        return self.data_info
    
    def get_column_names(self):
        """Get list of column names"""
        if self.data is not None:
            return list(self.data.columns)
        return []