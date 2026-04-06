# 🍔 Swiggy Food Delivery Analysis

A comprehensive data analysis project exploring **8,600+ restaurants** across **6+ Indian cities** from the Swiggy platform. Built with Python, Jupyter Notebook, Streamlit, Seaborn & Matplotlib.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualizations-3776AB)

---

## 📊 Project Overview

| Feature | Detail |
|---------|--------|
| **Dataset** | Swiggy restaurant data (8,681 rows) |
| **Cities** | Bangalore, Hyderabad, Mumbai, Pune, Kolkata, Chennai, Delhi |
| **Columns** | Restaurant, Area, City, Price, Rating, Votes, Cuisine, Delivery Time |
| **Tools** | Python, Pandas, Seaborn, Matplotlib, Plotly, Streamlit |

---

## 🏗️ Project Structure

```
sales/
├── data/
│   └── swiggy.csv              # Raw dataset
├── notebooks/
│   └── analysis.ipynb          # Full EDA Jupyter Notebook
├── assets/                     # Saved chart images
├── .streamlit/
│   └── config.toml             # Streamlit dark theme config
├── app.py                      # Streamlit interactive dashboard
├── utils.py                    # Shared data utilities
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## 🔍 Insights Analyzed

### ⭐ Core Insights
- Most popular cuisines (by count & ratings)
- Best-rated cuisines (100+ restaurant filter)
- Restaurant density by area
- Cost vs Rating correlation
- Average delivery time by location

### 🥇 Customer Value Analysis
- Best "Value for Money" restaurants (high rating + low cost)
- Top 10 budget-friendly restaurants

### 📍 Location Intelligence
- Cost variation across locations (box plots)
- Rating distribution per area (violin plots)
- Food Hubs — high density + high ratings

### ⏱️ Delivery Performance
- Fastest delivery cuisines
- Does faster delivery = better ratings?
- Delivery time by city comparison

### 🔍 Popularity vs Quality
- **Overhyped** — high votes but low rating
- **Hidden Gems** — low votes but high rating

### 🍽️ Cuisine Trends
- Multi-cuisine vs single cuisine performance
- Which cuisines dominate specific areas
- Cuisine popularity heatmap across cities

### 💡 Business Insights
- Optimal price range for highest ratings
- Best location + cuisine combo for new restaurant
- Dominant cuisines in top areas

---

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- pip

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/swiggy-food-delivery-analysis.git
cd swiggy-food-delivery-analysis
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Streamlit Dashboard
```bash
streamlit run app.py
```
The dashboard opens at `http://localhost:8501`

### Step 4: Run the Jupyter Notebook
```bash
cd notebooks
jupyter notebook analysis.ipynb
```

---

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Deploy! 🚀

### Vercel (Static Export)
> **Note:** Vercel doesn't natively support Python backends. Use Streamlit Cloud for the interactive dashboard. You can export notebook visualizations as static HTML for Vercel hosting.

---

## 📋 Key Findings

| Insight | Finding |
|---------|---------|
| Most Popular Cuisines | North Indian, Chinese, Fast Food |
| Cost vs Rating | Weak positive correlation — price ≠ quality |
| Best Value | Great ratings achievable at ₹100-300 |
| Hidden Gems | Many 4.5+ rated restaurants with <100 votes |
| Delivery | Avg ~55 min, no strong link to ratings |
| Business Tip | Mid-range pricing (₹400-600) gets best ratings |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Pandas & NumPy** — Data manipulation
- **Seaborn & Matplotlib** — Statistical visualizations
- **Plotly** — Interactive charts
- **Streamlit** — Web dashboard framework
- **Jupyter Notebook** — Exploratory data analysis

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ for data analysis portfolio
</p>
