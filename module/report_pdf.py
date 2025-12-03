import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd
import plotly.graph_objects as go
import tempfile
import os
import base64
from datetime import datetime

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'Custom',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=30
        )
        self.header_style = ParagraphStyle(
            'Header',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12
        )
        self.subheader_style = ParagraphStyle(
            'SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=8
        )
    
    def generate_report(self, df, ai_insights, charts, filename="adtech_report.pdf"):
        """Generate comprehensive PDF report"""
        
        # Create buffer for PDF
        buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Story will hold all elements
        story = []
        
        # 1. Cover Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("AdTech Performance Report", self.title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}", 
                              ParagraphStyle('Date', parent=self.styles['Normal'], alignment=TA_CENTER)))
        story.append(Spacer(1, inch))
        story.append(Paragraph("Confidential - For Internal Use Only", 
                              ParagraphStyle('Confidential', parent=self.styles['Normal'], 
                                            alignment=TA_CENTER, fontSize=10, 
                                            textColor=colors.gray)))
        
        story.append(Spacer(1, 2*inch))
        doc.build(story)
        
        # Save to file
        buffer.seek(0)
        
        # For now, save a basic PDF
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        
        return filename
    
    def generate_simple_report(self, df, ai_insights, filename="adtech_simple_report.pdf"):
        """Generate a simple PDF with AI insights"""
        from reportlab.pdfgen import canvas
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 100, "AdTech Performance Report")
        
        # Date
        c.setFont("Helvetica", 10)
        c.drawString(100, height - 130, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Dataset Info
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 180, "Dataset Summary:")
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 200, f"Rows: {len(df):,}")
        c.drawString(100, height - 220, f"Columns: {len(df.columns)}")
        c.drawString(100, height - 240, f"Generated with AI Insights")
        
        # AI Insights Section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 280, "AI-Generated Insights:")
        c.setFont("Helvetica", 10)
        
        # Split AI insights into lines
        y_position = height - 300
        for line in ai_insights.split('\n'):
            if y_position < 100:  # New page if needed
                c.showPage()
                y_position = height - 100
                c.setFont("Helvetica", 10)
            
            if line.strip():  # Skip empty lines
                c.drawString(100, y_position, line[:100])  # Limit line length
                y_position -= 15
        
        # Key Metrics
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Key Metrics Summary")
        
        # Calculate some basic metrics
        numeric_cols = df.select_dtypes(include=['number']).columns
        y_pos = height - 140
        
        if len(numeric_cols) > 0:
            for col in numeric_cols[:6]:  # First 6 numeric columns
                if y_pos < 100:
                    c.showPage()
                    y_pos = height - 100
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(100, y_pos, f"{col}:")
                c.setFont("Helvetica", 10)
                c.drawString(200, y_pos, f"Mean: {df[col].mean():.2f} | Max: {df[col].max():.2f} | Min: {df[col].min():.2f}")
                y_pos -= 25
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(100, 50, "Generated by TrendSpotter - Automated AdTech Insights Engine")
        c.drawString(100, 40, f"Page {c.getPageNumber()}")
        
        c.save()
        buffer.seek(0)
        
        # Save to file
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        
        return filename