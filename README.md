# 🚀 TrendSpotter: The Automated Insight Engine

**Tagline:** An event-driven data pipeline that converts raw CSV logs into executive-ready PDF/PPT reports with AI-generated narratives in under 30 seconds.

---

## 1. The Problem (Real World Scenario)

**Context:** In the AdTech world, we generate terabytes of data daily—foot traffic logs, ad clickstreams, and weather reports. Currently, Account Managers waste 4-6 hours every week manually downloading CSVs and taking screenshots to create "Weekly Performance Reports."

**The Pain Point:** This manual process is:
- **Slow:** Reporting lag causes delayed insights
- **Boring:** Repetitive, non-creative work
- **Error-prone:** Manual data handling introduces mistakes
- **Costly:** If a campaign is wasting budget, clients might not know for days

**My Solution:** TrendSpotter—an automated pipeline where you upload any data source (CSV, Excel, SQL), and within seconds, receive a fully analyzed, executive-ready PDF or PowerPoint report with AI-generated insights.

---

## 2. Expected End Result

**For the User:**
1. **Input:** Upload raw CSV/Excel or connect to SQL database via Streamlit UI
2. **Action:** Click "Generate Insights" (takes <30 seconds)
3. **Output:** Download professional PDF/PPT report containing:
   - Week-over-Week growth charts
   - Detected anomalies (e.g., "Conversion dropped 40% in Age Group 30-40")
   - AI-written executive summary explaining trends
   - Actionable recommendations for campaign optimization

---

## 3. Technical Approach

I built a production-ready ETL (Extract, Transform, Load) pipeline with intelligent automation.

**System Architecture:**
1. **Ingestion (Multi-Source):** Python script handles CSV, Excel, and SQL databases
2. **Processing Engine:** Polars/Pandas for fast data transformation
3. **AI Analysis:** Google Gemini Pro for natural language insights generation
4. **Anomaly Detection:** Statistical analysis to identify outliers
5. **Reporting:** Automated PDF and PowerPoint generation
6. **Dashboard:** Streamlit UI for easy interaction

**Key Technical Decisions:**
- **Polars over Pandas:** For larger datasets with better performance
- **Gemini over GPT:** Cost-effective with excellent text generation
- **Streamlit:** Rapid prototyping with professional UI
- **Event-Driven:** Folder watching for automated processing (optional mode)

**Guardrails Implemented:**
- **Data Validation:** Schema enforcement to prevent processing errors
- **AI Context Limiting:** Strict prompts to prevent hallucinations
- **Template System:** Consistent professional reporting format

---

## 4. Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.11 | Core programming language |
| **Data Processing** | Polars, Pandas | Fast DataFrame operations |
| **AI/ML** | Google Gemini  | Natural language insights |
| **Visualization** | Plotly, Matplotlib | Interactive charts |
| **Reporting** | ReportLab, python-pptx | PDF & PowerPoint generation |
| **UI/Dashboard** | Streamlit | User interface |
| **Database Connectors** | SQLAlchemy | SQL database integration |

---
## 5. Challenges & Learnings

This project wasn't easy. Here are two major hurdles I overcame:

**Challenge 1: AI Hallucinations**

**Issue:** Initially, the AI would invent reasons for data drops (e.g., claiming "It rained" when I provided no weather data).

**Solution:** I implemented a "Strict Context" System Prompt. I effectively told the AI: "Only use the data provided in the JSON context. If you don't know, say 'Unknown'." This reduced hallucination rates significantly.

**Challenge 2: Multi-Format Reporting**

**Issue:** Creating consistent professional reports across both PDF and PowerPoint formats.

**Solution:** Built template-based system with standardized layouts. Both report types now use the same data and insights, ensuring consistency while maintaining format-specific optimizations.

---

## 6. Visual Proof

![Dashboard Interface](screenshots/dashboard.png)

*Streamlit dashboard showing data upload and AI analysis*

![PDF Report](screenshots/pdf_report.png)

*Professional PDF report with charts and AI insights*

![Terminal Output](screenshots/terminal.png)

*Terminal showing automated pipeline execution*

## 7. How to Run

### **Quick Start (Development):**
```bash
# 1. Clone repository
git clone https://github.com/yourusername/trendspotter.git
cd trendspotter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Run the application
streamlit run app.py
