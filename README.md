# Swiggy Food Delivery Analysis

A comprehensive data analysis project exploring **8,600+ restaurants** across **9 Indian cities** from the Swiggy platform. Built with Python, Streamlit, Plotly, Seaborn & Matplotlib.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?logo=plotly)

---

## Project Overview

| Feature | Detail |
|---------|--------|
| **Dataset** | Swiggy restaurant data (8,681 rows) |
| **Cities** | Bangalore, Hyderabad, Mumbai, Pune, Kolkata, Chennai, Delhi, Surat, Ahmedabad |
| **Columns** | Restaurant, Area, City, Price, Rating, Votes, Cuisine, Delivery Time |
| **Tools** | Python, Pandas, NumPy, Seaborn, Matplotlib, Plotly, Streamlit, Lottie |
| **Theme** | Dark Glassmorphism with gradient accents |

---

## Dashboard Sections (11 Total)

### Core Analytics
- **Overview** — KPI cards, city distribution, rating histogram, top areas
- **Cuisine Analysis** — Top cuisines, best rated, heatmap, multi vs single cuisine
- **Location Intelligence** — Restaurant density, cost/rating by area, food hubs, fastest areas
- **Value Analysis** — Cost vs rating correlation, value-for-money, budget-friendly picks
- **Delivery Performance** — Distribution, delivery vs rating, fastest cuisines, city comparison
- **Hidden Gems & Overhyped** — Under-the-radar gems and overrated restaurants
- **Business Insights** — Optimal price range, location-cuisine combos, dominant cuisines

### Advanced Features (NEW)
- **Restaurant Finder** — Full-text search with multi-filter explorer
- **Compare & Discover** — Radar chart comparisons for restaurants and cuisines, competition heatmap
- **City Benchmarks** — City comparison table, radar charts, Shannon diversity index
- **Smart Recommendations** — Preference-based recommendation engine with match scores, similar restaurant finder

---

## Key Findings

| Insight | Finding |
|---------|---------|
| Most Popular Cuisines | North Indian, Chinese, Fast Food |
| Cost vs Rating | Weak positive correlation — price does not equal quality |
| Best Value | Great ratings achievable at Rs.100-300 |
| Hidden Gems | Many 4.5+ rated restaurants with <100 votes |
| Delivery | Avg ~55 min, no strong link to ratings |
| Business Tip | Mid-range pricing (Rs.400-600) gets best ratings |

---

## How to Run

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

### Step 3: Run the Dashboard
```bash
streamlit run app.py
```
The dashboard opens at `http://localhost:8501`

---

## Tech Stack

- **Python** — Core language
- **Pandas & NumPy** — Data manipulation
- **Seaborn & Matplotlib** — Statistical visualizations
- **Plotly** — Interactive charts & radar plots
- **Streamlit** — Web dashboard framework
- **Streamlit-Lottie** — Loading animations
- **Statsmodels** — Regression trendlines

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with love for data analysis portfolio | Dark Glass Edition
</p>
