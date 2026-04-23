"""
Swiggy Food Delivery Analysis - Interactive Dashboard
Built with Streamlit, Plotly, Seaborn & Matplotlib
Dark Glassmorphism Edition
"""
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go
import json, requests
from streamlit_lottie import st_lottie
from utils import (
    load_data, explode_cuisines, get_top_cuisines, get_best_rated_cuisines,
    get_location_density, get_value_for_money, get_budget_friendly,
    get_food_hubs, get_hidden_gems, get_overhyped, get_delivery_by_cuisine,
    get_optimal_price_range, get_best_location_cuisine_combo,
    search_restaurants, get_restaurant_comparison_data, get_cuisine_radar_data,
    get_cuisine_competition, get_city_benchmarks, get_city_cuisine_diversity,
    recommend_restaurants, get_similar_restaurants, get_export_csv,
)

st.set_page_config(page_title="Swiggy Food Delivery Analysis", page_icon="\U0001F354", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, html, body, [class*="st-"] { font-family: 'Inter', sans-serif !important; }
.main { background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%); }
section[data-testid="stSidebar"] > div { background: linear-gradient(180deg, rgba(26,26,46,0.95) 0%, rgba(15,15,26,0.98) 100%) !important; border-right: 1px solid rgba(224,64,251,0.15) !important; }
.glass { background: rgba(255,255,255,0.04); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; }
.kpi-row { display: flex; gap: 16px; margin: 16px 0 28px; flex-wrap: wrap; }
.kpi-card { flex: 1; min-width: 150px; background: rgba(255,255,255,0.04); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 22px 16px; text-align: center; transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s; }
.kpi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 32px rgba(224,64,251,0.15); border-color: rgba(224,64,251,0.3); }
.kpi-icon { font-size: 1.7rem; margin-bottom: 6px; }
.kpi-value { font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #E040FB, #FF6090); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; }
.kpi-label { font-size: 0.7rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1.4px; font-weight: 600; margin-top: 8px; }
.section-header { font-size: 1.3rem; font-weight: 700; background: linear-gradient(90deg, #E040FB, #536DFE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 28px 0 14px; padding-bottom: 10px; border-bottom: 2px solid rgba(224,64,251,0.2); }
.insight-box { background: rgba(224,64,251,0.06); border-left: 4px solid #E040FB; border-radius: 0 12px 12px 0; padding: 14px 18px; margin: 14px 0; color: rgba(255,255,255,0.85); font-size: 0.92rem; line-height: 1.6; backdrop-filter: blur(8px); }
h1 { background: linear-gradient(135deg, #E040FB, #536DFE, #00E5FF) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-weight: 800 !important; }
h2, h3 { color: rgba(255,255,255,0.9) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(255,255,255,0.03); border-radius: 12px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 8px 20px; font-weight: 600; color: rgba(255,255,255,0.6) !important; }
.stTabs [aria-selected="true"] { background: rgba(224,64,251,0.15) !important; color: #E040FB !important; }
.stDataFrame { border-radius: 12px; overflow: hidden; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(224,64,251,0.3); border-radius: 3px; }
.stDownloadButton > button { background: rgba(224,64,251,0.12) !important; border: 1px solid rgba(224,64,251,0.3) !important; color: #E040FB !important; border-radius: 10px !important; transition: all 0.3s !important; }
.stDownloadButton > button:hover { background: rgba(224,64,251,0.25) !important; box-shadow: 0 4px 20px rgba(224,64,251,0.2) !important; }
div[data-baseweb="select"] > div { background: rgba(255,255,255,0.05) !important; border-color: rgba(255,255,255,0.1) !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

LOTTIE_FOOD = "https://lottie.host/b3845e5b-22f4-4b3e-be7f-5b3e6e146152/QrJHlHjnTX.json"

@st.cache_data
def get_data():
    df = load_data()
    df_exp = explode_cuisines(df)
    return df, df_exp

df_raw, df_exploded = get_data()

with st.sidebar:
    st.markdown("## Swiggy Analysis")
    st.markdown("---")
    cities = ["All"] + sorted(df_raw["City"].unique().tolist())
    selected_city = st.selectbox("Select City", cities, index=0)
    st.markdown("---")
    sections = [
        "Overview", "Cuisine Analysis", "Location Intelligence",
        "Value Analysis", "Delivery Performance", "Hidden Gems & Overhyped",
        "Business Insights", "Restaurant Finder", "Compare & Discover",
        "City Benchmarks", "Smart Recommendations",
    ]
    selected_section = st.radio("Navigate", sections, index=0)
    st.markdown("---")
    st.caption("Built with Streamlit | Dark Glass Edition")

if selected_city != "All":
    df = df_raw[df_raw["City"] == selected_city].copy()
    df_exp = df_exploded[df_exploded["City"] == selected_city].copy()
else:
    df = df_raw.copy()
    df_exp = df_exploded.copy()

def set_plot_style():
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({
        "figure.facecolor": "#0F0F1A", "axes.facecolor": "#1A1A2E",
        "axes.edgecolor": "#2A2A4A", "axes.labelcolor": "#C0C0C0",
        "xtick.color": "#A0A0A0", "ytick.color": "#A0A0A0",
        "text.color": "#D0D0D0", "grid.color": "#2A2A4A", "grid.alpha": 0.4,
        "font.family": "sans-serif", "font.size": 11,
    })

PALETTE = ["#E040FB", "#536DFE", "#00E5FF", "#69F0AE", "#FFD740",
           "#FF6E40", "#EA80FC", "#448AFF", "#18FFFF", "#B2FF59",
           "#FF9100", "#7C4DFF", "#64FFDA", "#FFAB40", "#FF5252"]
set_plot_style()

def render_kpis(items):
    cards = ""
    for icon, value, label in items:
        cards += f'<div class="kpi-card"><div class="kpi-icon">{icon}</div><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div>'
    st.markdown(f'<div class="kpi-row">{cards}</div>', unsafe_allow_html=True)

DARK_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#ccc"))

# ---- SECTION 1: OVERVIEW ----
if selected_section == "Overview":
    st.markdown("# Swiggy Food Delivery Analysis")
    lottie = load_lottie_url(LOTTIE_FOOD)
    city_label = selected_city if selected_city != "All" else f"{df['City'].nunique()} cities"
    if lottie:
        cl, cr = st.columns([3, 1])
        with cl:
            st.markdown(f"*Analyzing **{len(df):,}** restaurants across **{city_label}***")
        with cr:
            st_lottie(lottie, height=90, key="hero")
    else:
        st.markdown(f"*Analyzing **{len(df):,}** restaurants across **{city_label}***")
    render_kpis([
        ("R", f"{len(df):,}", "Total Restaurants"),
        ("S", f"{df['Rating'].mean():.2f}", "Avg Rating"),
        ("C", f"Rs.{df['Cost_for_Two'].mean():.0f}", "Avg Cost for Two"),
        ("T", f"{df['Delivery_Time'].mean():.0f} min", "Avg Delivery Time"),
        ("Q", f"{df_exp['Cuisine'].nunique()}", "Unique Cuisines"),
    ])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">City Distribution</div>', unsafe_allow_html=True)
        city_counts = df["City"].value_counts()
        fig = px.pie(values=city_counts.values, names=city_counts.index, hole=0.55, color_discrete_sequence=PALETTE)
        fig.update_layout(**DARK_LAYOUT, height=420, margin=dict(t=10, b=10), legend=dict(font=dict(size=11, color="#aaa")))
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="section-header">Rating Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5.2))
        sns.histplot(df["Rating"], bins=20, kde=True, color="#E040FB", ax=ax, edgecolor="#1A1A2E", alpha=0.8)
        ax.axvline(df["Rating"].mean(), color="#00E5FF", linestyle="--", linewidth=2, label=f"Mean: {df['Rating'].mean():.2f}")
        ax.set_xlabel("Rating"); ax.set_ylabel("Count")
        ax.legend(fontsize=11, frameon=True, facecolor="#1A1A2E", edgecolor="#2A2A4A", labelcolor="#ccc")
        plt.tight_layout(); st.pyplot(fig); plt.close()
    st.markdown('<div class="section-header">Top 10 Areas by Restaurant Count</div>', unsafe_allow_html=True)
    top_areas = df["Area"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.barh(top_areas.index[::-1], top_areas.values[::-1], color=PALETTE[:10], edgecolor="#1A1A2E", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{int(bar.get_width())}', va='center', fontsize=11, color="#ccc", fontweight="bold")
    ax.set_xlabel("Number of Restaurants"); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ---- SECTION 2: CUISINE ANALYSIS ----
elif selected_section == "Cuisine Analysis":
    st.markdown("# Cuisine Analysis")
    render_kpis([
        ("P", f"{df_exp['Cuisine'].nunique()}", "Unique Cuisines"),
        ("W", f"{df_exp.groupby('Cuisine').size().idxmax()}", "Most Popular"),
        ("M", f"{df['Cuisine_Type'].value_counts().get('Multi', 0):,}", "Multi-Cuisine"),
        ("S", f"{df['Cuisine_Type'].value_counts().get('Single', 0):,}", "Single-Cuisine"),
    ])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Top 15 Most Popular Cuisines</div>', unsafe_allow_html=True)
        top_cuisines = get_top_cuisines(df_exp, 15)
        fig, ax = plt.subplots(figsize=(8, 7))
        bars = ax.barh(top_cuisines["Cuisine"].values[::-1], top_cuisines["Count"].values[::-1], color=PALETTE[:15][::-1], edgecolor="#1A1A2E", height=0.7)
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'{int(bar.get_width())}', va='center', fontsize=10, color="#ccc", fontweight="bold")
        ax.set_xlabel("Number of Restaurants"); ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-header">Best Rated Cuisines (100+ restaurants)</div>', unsafe_allow_html=True)
        best_rated = get_best_rated_cuisines(df_exp, min_restaurants=100, n=15)
        if len(best_rated) > 0:
            fig, ax = plt.subplots(figsize=(8, 7))
            colors = [PALETTE[i % len(PALETTE)] for i in range(len(best_rated))]
            bars = ax.barh(best_rated["Cuisine"].values[::-1], best_rated["Avg_Rating"].values[::-1], color=colors[::-1], edgecolor="#1A1A2E", height=0.7)
            for bar in bars:
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.2f}', va='center', fontsize=10, color="#ccc", fontweight="bold")
            ax.set_xlabel("Average Rating"); ax.set_xlim(left=3.5); ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout(); st.pyplot(fig); plt.close()
        else:
            st.info("Not enough data. Try selecting All cities.")
    st.markdown('<div class="section-header">Cuisine Popularity Across Cities</div>', unsafe_allow_html=True)
    top_10_cuisines = df_exploded.groupby("Cuisine").size().nlargest(10).index.tolist()
    heatmap_data = df_exploded[df_exploded["Cuisine"].isin(top_10_cuisines)]
    pivot = heatmap_data.pivot_table(index="Cuisine", columns="City", values="Restaurant", aggfunc="count", fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 5.5))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="magma", linewidths=1, linecolor="#1A1A2E", ax=ax, cbar_kws={"shrink": 0.8}, annot_kws={"color": "white"})
    ax.set_xlabel("City", fontsize=12); ax.set_ylabel("Cuisine", fontsize=12); ax.tick_params(colors="#aaa")
    plt.tight_layout(); st.pyplot(fig); plt.close()
    st.markdown('<div class="section-header">Multi-Cuisine vs Single-Cuisine Performance</div>', unsafe_allow_html=True)
    cuisine_type_stats = df.groupby("Cuisine_Type").agg(Avg_Rating=("Rating", "mean"), Avg_Cost=("Cost_for_Two", "mean"), Count=("Restaurant", "count"), Avg_Delivery=("Delivery_Time", "mean")).reset_index()
    c1, c2, c3 = st.columns(3)
    for title, col, container, ylim in [("Avg Rating", "Avg_Rating", c1, (3.5, 4.5)), ("Avg Cost (Rs.)", "Avg_Cost", c2, None), ("Avg Delivery (min)", "Avg_Delivery", c3, None)]:
        with container:
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.bar(cuisine_type_stats["Cuisine_Type"], cuisine_type_stats[col], color=["#E040FB", "#00E5FF"], edgecolor="#1A1A2E", width=0.5)
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01, f'{bar.get_height():.2f}', ha='center', fontsize=12, color="#ccc", fontweight="bold")
            ax.set_ylabel(title); ax.set_title(title, fontsize=13, fontweight="bold", color="#ccc")
            if ylim: ax.set_ylim(ylim)
            ax.spines[["top", "right"]].set_visible(False); plt.tight_layout(); st.pyplot(fig); plt.close()

# ---- SECTION 3: LOCATION INTELLIGENCE ----
elif selected_section == "Location Intelligence":
    st.markdown("# Location Intelligence")
    st.markdown('<div class="section-header">Top 20 Areas by Restaurant Density</div>', unsafe_allow_html=True)
    density = get_location_density(df, top_n=20)
    fig = px.bar(density, x="Area", y="Restaurant_Count", color="Avg_Rating", color_continuous_scale="Magma", text="Restaurant_Count", labels={"Restaurant_Count": "Restaurants", "Avg_Rating": "Avg Rating"})
    fig.update_layout(**DARK_LAYOUT, height=450, margin=dict(t=20), xaxis=dict(tickangle=-45))
    fig.update_traces(textposition="outside", textfont_size=10)
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Cost Variation Across Top Areas</div>', unsafe_allow_html=True)
        top_a = df["Area"].value_counts().head(10).index.tolist()
        df_top = df[df["Area"].isin(top_a)]
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df_top, x="Area", y="Cost_for_Two", palette=PALETTE[:10], ax=ax, flierprops=dict(marker="o", markerfacecolor="#E040FB", markersize=3, alpha=0.5))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.set_xlabel(""); ax.set_ylabel("Cost for Two (Rs.)"); ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-header">Rating Distribution per Area</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.violinplot(data=df_top, x="Area", y="Rating", palette=PALETTE[:10], ax=ax, inner="quartile")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.set_xlabel(""); ax.set_ylabel("Rating"); ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
    st.markdown('<div class="section-header">Food Hubs (High Density + High Ratings)</div>', unsafe_allow_html=True)
    hubs = get_food_hubs(df, min_restaurants=10, min_avg_rating=4.0)
    if len(hubs) > 0:
        fig = px.scatter(hubs, x="Restaurant_Count", y="Avg_Rating", size="Avg_Cost", color="Avg_Delivery", text="Area", color_continuous_scale="Magma", labels={"Restaurant_Count": "Restaurants", "Avg_Rating": "Rating", "Avg_Cost": "Avg Cost", "Avg_Delivery": "Delivery (min)"})
        fig.update_traces(textposition="top center", textfont_size=9, textfont_color="#ccc")
        fig.update_layout(**DARK_LAYOUT, height=500, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Food Hubs = areas with 10+ restaurants AND avg rating >= 4.0. Bubble size = avg cost, color = delivery time.</div>', unsafe_allow_html=True)
    else:
        st.info("No food hubs found with current filters.")
    st.markdown('<div class="section-header">Fastest Delivery Areas</div>', unsafe_allow_html=True)
    delivery_by_area = df.groupby("Area")["Delivery_Time"].agg(["mean", "count"]).reset_index().query("count >= 10").sort_values("mean")
    top_fast = delivery_by_area.head(15)
    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.barh(top_fast["Area"].values[::-1], top_fast["mean"].values[::-1], color="#00E5FF", edgecolor="#1A1A2E", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f} min', va='center', fontsize=10, color="#ccc", fontweight="bold")
    ax.set_xlabel("Avg Delivery Time (min)"); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ---- SECTION 4: VALUE ANALYSIS ----
elif selected_section == "Value Analysis":
    st.markdown("# Customer Value Analysis")
    st.markdown('<div class="section-header">Cost vs Rating Correlation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        fig = px.scatter(df, x="Cost_for_Two", y="Rating", color="City", opacity=0.4, size_max=8, color_discrete_sequence=PALETTE, labels={"Cost_for_Two": "Cost for Two (Rs.)", "Rating": "Rating"}, trendline="ols")
        fig.update_layout(**DARK_LAYOUT, height=480, margin=dict(t=20), legend=dict(font=dict(size=10, color="#aaa")))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        corr = df["Cost_for_Two"].corr(df["Rating"])
        st.markdown(f'<div class="kpi-card" style="margin-top:40px;"><div class="kpi-icon">C</div><div class="kpi-value">{corr:.3f}</div><div class="kpi-label">Correlation</div></div>', unsafe_allow_html=True)
        if abs(corr) < 0.15:
            st.markdown('<div class="insight-box"><b>Weak correlation</b> - Price has negligible impact on ratings. Affordable restaurants can be just as good!</div>', unsafe_allow_html=True)
        elif corr > 0:
            st.markdown('<div class="insight-box"><b>Positive correlation</b> - Pricier restaurants tend to rate slightly higher.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="insight-box"><b>Negative correlation</b> - Higher price does NOT guarantee better ratings.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Best Value-for-Money Restaurants</div>', unsafe_allow_html=True)
    vfm = get_value_for_money(df, top_n=10)
    display_cols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Cuisine", "Value_Score"]
    st.dataframe(vfm[display_cols].style.background_gradient(subset=["Value_Score"], cmap="magma").format({"Rating": "{:.1f}", "Value_Score": "{:.2f}", "Cost_for_Two": "Rs.{:.0f}"}), use_container_width=True, hide_index=True)
    st.download_button("Export Value Data", get_export_csv(vfm, display_cols), "value_for_money.csv", "text/csv", key="dl_vfm")
    st.markdown('<div class="section-header">Top 10 Budget-Friendly Restaurants</div>', unsafe_allow_html=True)
    col_cost, col_rating = st.columns(2)
    with col_cost: max_cost = st.slider("Max Cost for Two (Rs.)", 100, 500, 300, step=50)
    with col_rating: min_rating = st.slider("Min Rating", 3.0, 5.0, 4.0, step=0.1)
    budget = get_budget_friendly(df, max_cost=max_cost, min_rating=min_rating, top_n=10)
    if len(budget) > 0:
        bcols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Cuisine", "Delivery_Time"]
        st.dataframe(budget[bcols].style.background_gradient(subset=["Rating"], cmap="viridis").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}", "Delivery_Time": "{:.0f} min"}), use_container_width=True, hide_index=True)
        st.download_button("Export Budget Picks", get_export_csv(budget, bcols), "budget_friendly.csv", "text/csv", key="dl_budget")
    else:
        st.warning("No restaurants found with these filters. Try adjusting the sliders.")

# ---- SECTION 5: DELIVERY PERFORMANCE ----
elif selected_section == "Delivery Performance":
    st.markdown("# Delivery Performance")
    render_kpis([
        ("F", f"{df['Delivery_Time'].min():.0f} min", "Fastest"),
        ("S", f"{df['Delivery_Time'].max():.0f} min", "Slowest"),
        ("A", f"{df['Delivery_Time'].mean():.1f} min", "Average"),
        ("M", f"{df['Delivery_Time'].median():.0f} min", "Median"),
    ])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Delivery Time Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df["Delivery_Time"], bins=30, kde=True, color="#536DFE", ax=ax, edgecolor="#1A1A2E", alpha=0.8)
        ax.axvline(df["Delivery_Time"].mean(), color="#E040FB", linestyle="--", linewidth=2, label=f"Mean: {df['Delivery_Time'].mean():.1f} min")
        ax.set_xlabel("Delivery Time (min)"); ax.set_ylabel("Count")
        ax.legend(fontsize=11, frameon=True, facecolor="#1A1A2E", edgecolor="#2A2A4A", labelcolor="#ccc")
        ax.spines[["top", "right"]].set_visible(False); plt.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-header">Delivery Time vs Rating</div>', unsafe_allow_html=True)
        fig = px.scatter(df, x="Delivery_Time", y="Rating", opacity=0.2, color_discrete_sequence=["#536DFE"], trendline="ols", labels={"Delivery_Time": "Delivery Time (min)"})
        corr = df["Delivery_Time"].corr(df["Rating"])
        fig.update_layout(**DARK_LAYOUT, height=400, margin=dict(t=40), title=dict(text=f"Correlation: {corr:.3f}", font=dict(color="#E040FB")))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="section-header">Fastest Delivery Cuisines (50+ restaurants)</div>', unsafe_allow_html=True)
    fast_cuisines = get_delivery_by_cuisine(df_exp, top_n=15)
    fig, ax = plt.subplots(figsize=(14, 5.5))
    bars = ax.barh(fast_cuisines["Cuisine"].values[::-1], fast_cuisines["Avg_Delivery"].values[::-1], color=PALETTE[:len(fast_cuisines)][::-1], edgecolor="#1A1A2E", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f} min', va='center', fontsize=10, color="#ccc", fontweight="bold")
    ax.set_xlabel("Avg Delivery Time (min)"); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()
    st.markdown('<div class="section-header">Delivery Time by City</div>', unsafe_allow_html=True)
    city_delivery = df_raw.groupby("City")["Delivery_Time"].mean().sort_values()
    fig = px.bar(x=city_delivery.index, y=city_delivery.values, text=city_delivery.values, color=city_delivery.values, color_continuous_scale="Magma_r", labels={"x": "City", "y": "Avg Delivery Time (min)"})
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(**DARK_LAYOUT, height=400, margin=dict(t=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---- SECTION 6: HIDDEN GEMS & OVERHYPED ----
elif selected_section == "Hidden Gems & Overhyped":
    st.markdown("# Hidden Gems & Overhyped Restaurants")
    tab1, tab2 = st.tabs(["Hidden Gems", "Overhyped"])
    with tab1:
        st.markdown('<div class="section-header">Hidden Gems</div>', unsafe_allow_html=True)
        col_v, col_r = st.columns(2)
        with col_v: gem_max_votes = st.slider("Max Votes", 20, 500, 100, step=10, key="gem_votes")
        with col_r: gem_min_rating = st.slider("Min Rating", 4.0, 5.0, 4.5, step=0.1, key="gem_rating")
        gems = get_hidden_gems(df, max_votes=gem_max_votes, min_rating=gem_min_rating, top_n=15)
        if len(gems) > 0:
            gcols = ["Restaurant", "Area", "City", "Rating", "Votes", "Cost_for_Two", "Cuisine"]
            st.dataframe(gems[gcols].style.background_gradient(subset=["Rating"], cmap="viridis").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}"}), use_container_width=True, hide_index=True)
            st.download_button("Export Hidden Gems", get_export_csv(gems, gcols), "hidden_gems.csv", "text/csv", key="dl_gems")
            fig, ax = plt.subplots(figsize=(14, 5))
            bars = ax.barh(gems["Restaurant"].values[::-1], gems["Rating"].values[::-1], color="#69F0AE", edgecolor="#1A1A2E", height=0.65)
            for bar, votes in zip(bars, gems["Votes"].values[::-1]):
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f} ({int(votes)} votes)', va='center', fontsize=9, color="#ccc")
            ax.set_xlabel("Rating"); ax.set_xlim(left=4.0); ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout(); st.pyplot(fig); plt.close()
            st.markdown('<div class="insight-box">These restaurants have excellent ratings but have not gained popularity yet. Great picks for adventurous foodies!</div>', unsafe_allow_html=True)
        else:
            st.info("No hidden gems found. Try adjusting the filters.")
    with tab2:
        st.markdown('<div class="section-header">Overhyped Restaurants</div>', unsafe_allow_html=True)
        col_v2, col_r2 = st.columns(2)
        with col_v2: oh_min_votes = st.slider("Min Votes", 500, 10000, 1000, step=500, key="oh_votes")
        with col_r2: oh_max_rating = st.slider("Max Rating", 2.0, 4.0, 3.5, step=0.1, key="oh_rating")
        overhyped = get_overhyped(df, min_votes=oh_min_votes, max_rating=oh_max_rating, top_n=15)
        if len(overhyped) > 0:
            ocols = ["Restaurant", "Area", "City", "Rating", "Votes", "Cost_for_Two", "Cuisine"]
            st.dataframe(overhyped[ocols].style.background_gradient(subset=["Rating"], cmap="magma_r").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}"}), use_container_width=True, hide_index=True)
            st.download_button("Export Overhyped", get_export_csv(overhyped, ocols), "overhyped.csv", "text/csv", key="dl_oh")
            fig = px.scatter(overhyped, x="Votes", y="Rating", size="Cost_for_Two", text="Restaurant", color_discrete_sequence=["#FF5252"], labels={"Votes": "Total Votes", "Cost_for_Two": "Cost"})
            fig.update_traces(textposition="top center", textfont_size=9, textfont_color="#ccc")
            fig.update_layout(**DARK_LAYOUT, height=450, margin=dict(t=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="insight-box">These restaurants are widely known but underperform on ratings. High visibility does not equal high quality.</div>', unsafe_allow_html=True)
        else:
            st.info("No overhyped restaurants found. Try adjusting the filters.")

# ---- SECTION 7: BUSINESS INSIGHTS ----
elif selected_section == "Business Insights":
    st.markdown("# Business Insights")
    st.markdown('<div class="section-header">Optimal Price Range for Highest Ratings</div>', unsafe_allow_html=True)
    price_stats = get_optimal_price_range(df)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(price_stats, x="Price_Range", y="Avg_Rating", text="Avg_Rating", color="Avg_Rating", color_continuous_scale="Magma", labels={"Price_Range": "Price Range", "Avg_Rating": "Avg Rating"})
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(**DARK_LAYOUT, height=420, margin=dict(t=20), yaxis=dict(range=[3.3, 4.6]), showlegend=False, title=dict(text="Avg Rating by Price Range", font=dict(color="#E040FB")))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(price_stats, x="Price_Range", y="Count", text="Count", color_discrete_sequence=["#536DFE"], labels={"Price_Range": "Price Range", "Count": "Restaurants"})
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(**DARK_LAYOUT, height=420, margin=dict(t=20), title=dict(text="Restaurant Count by Price Range", font=dict(color="#536DFE")))
        st.plotly_chart(fig, use_container_width=True)
    best_range = price_stats.loc[price_stats["Avg_Rating"].idxmax(), "Price_Range"]
    st.markdown(f'<div class="insight-box"><b>Optimal Price Range:</b> Restaurants in the <b>{best_range}</b> bracket achieve the highest average rating.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Best Location + Cuisine Combos for New Restaurant</div>', unsafe_allow_html=True)
    combos = get_best_location_cuisine_combo(df_exp, top_n=15)
    if len(combos) > 0:
        st.dataframe(combos[["Area", "Cuisine", "Count", "Avg_Rating", "Avg_Cost", "Score"]].rename(columns={"Count": "Existing", "Avg_Rating": "Avg Rating", "Avg_Cost": "Avg Cost Rs.", "Score": "Opportunity"}).style.background_gradient(subset=["Opportunity"], cmap="magma").format({"Avg Rating": "{:.2f}", "Avg Cost Rs.": "Rs.{:.0f}", "Opportunity": "{:.2f}"}), use_container_width=True, hide_index=True)
        st.download_button("Export Combos", get_export_csv(combos), "location_cuisine_combos.csv", "text/csv", key="dl_combos")
        st.markdown('<div class="insight-box"><b>Opportunity Score</b> = Rating x log(Count). High scores indicate proven demand + quality in that area-cuisine pair.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Dominant Cuisines in Top Areas</div>', unsafe_allow_html=True)
    top_areas_biz = df["Area"].value_counts().head(8).index.tolist()
    df_top_biz = df_exp[df_exp["Area"].isin(top_areas_biz)]
    dominant = df_top_biz.groupby(["Area", "Cuisine"]).size().reset_index(name="Count").sort_values(["Area", "Count"], ascending=[True, False])
    dominant_top = dominant.groupby("Area").head(5).reset_index(drop=True)
    fig = px.bar(dominant_top, x="Area", y="Count", color="Cuisine", barmode="group", color_discrete_sequence=PALETTE, labels={"Count": "Restaurants"})
    fig.update_layout(**DARK_LAYOUT, height=480, margin=dict(t=20), legend=dict(font=dict(size=10, color="#aaa")), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig, use_container_width=True)

# ---- SECTION 8: RESTAURANT FINDER ----
elif selected_section == "Restaurant Finder":
    st.markdown("# Restaurant Finder")
    st.markdown('<div class="insight-box">Search by name, area, or cuisine. Combine filters to narrow results.</div>', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1: query = st.text_input("Search", placeholder="Restaurant, area, or cuisine...")
    with fc2:
        all_cuisines = ["All"] + sorted(df_exp["Cuisine"].unique().tolist())
        cuisine_filter = st.selectbox("Cuisine", all_cuisines, key="finder_cuisine")
    with fc3: sort_by = st.selectbox("Sort By", ["Rating", "Cost (Low to High)", "Cost (High to Low)", "Delivery Time", "Popularity (Votes)"])
    fc4, fc5 = st.columns(2)
    with fc4: price_range = st.slider("Price Range (Rs.)", 0, 2000, (0, 1000), step=50, key="finder_price")
    with fc5: min_r = st.slider("Min Rating", 0.0, 5.0, 0.0, step=0.1, key="finder_rating")
    results = search_restaurants(df, query=query, city=selected_city, cuisine_filter=cuisine_filter, min_price=price_range[0], max_price=price_range[1], min_rating=min_r, sort_by=sort_by, top_n=50)
    render_kpis([
        ("N", f"{len(results)}", "Results Found"),
        ("R", f"{results['Rating'].mean():.2f}" if len(results) else "-", "Avg Rating"),
        ("C", f"Rs.{results['Cost_for_Two'].mean():.0f}" if len(results) else "-", "Avg Cost"),
        ("D", f"{results['Delivery_Time'].mean():.0f} min" if len(results) else "-", "Avg Delivery"),
    ])
    if len(results) > 0:
        show_cols = ["Restaurant", "Area", "City", "Rating", "Votes", "Cost_for_Two", "Cuisine", "Delivery_Time"]
        st.dataframe(results[show_cols].style.background_gradient(subset=["Rating"], cmap="viridis").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}", "Delivery_Time": "{:.0f} min"}), use_container_width=True, hide_index=True)
        st.download_button("Export Results", get_export_csv(results, show_cols), "search_results.csv", "text/csv", key="dl_search")
    else:
        st.warning("No restaurants match your criteria. Try broadening the filters.")

# ---- SECTION 9: COMPARE & DISCOVER ----
elif selected_section == "Compare & Discover":
    st.markdown("# Compare & Discover")
    tab_r, tab_c, tab_comp = st.tabs(["Restaurant vs Restaurant", "Cuisine vs Cuisine", "Competition Map"])
    with tab_r:
        st.markdown('<div class="section-header">Restaurant Radar Comparison</div>', unsafe_allow_html=True)
        rest_names = sorted(df["Restaurant"].unique().tolist())
        selected_rests = st.multiselect("Select 2-4 Restaurants", rest_names, default=rest_names[:2] if len(rest_names) >= 2 else rest_names, max_selections=4, key="cmp_rest")
        if len(selected_rests) >= 2:
            cmp_data = get_restaurant_comparison_data(df, selected_rests)
            if len(cmp_data) >= 2:
                categories = ["Rating", "Affordability", "Speed", "Popularity"]
                fig = go.Figure()
                for _, row in cmp_data.iterrows():
                    fig.add_trace(go.Scatterpolar(r=[row["Rating_norm"], row["Cost_for_Two_norm"], row["Delivery_Time_norm"], row["Votes_norm"]], theta=categories, fill='toself', name=row["Restaurant"], line=dict(width=2)))
                fig.update_layout(polar=dict(bgcolor="rgba(255,255,255,0.02)", radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"), angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")), **DARK_LAYOUT, height=480, margin=dict(t=40), showlegend=True, legend=dict(font=dict(color="#aaa")))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('<div class="section-header">Side-by-Side Stats</div>', unsafe_allow_html=True)
                stats_cols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Delivery_Time", "Votes", "Cuisine"]
                st.dataframe(cmp_data[[c for c in stats_cols if c in cmp_data.columns]].style.format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}", "Delivery_Time": "{:.0f} min"}).background_gradient(subset=["Rating"], cmap="viridis"), use_container_width=True, hide_index=True)
            else:
                st.info("Could not find enough matching restaurants.")
        else:
            st.info("Select at least 2 restaurants to compare.")
    with tab_c:
        st.markdown('<div class="section-header">Cuisine Radar Comparison</div>', unsafe_allow_html=True)
        all_c = sorted(df_exp["Cuisine"].value_counts().head(30).index.tolist())
        sel_cuisines = st.multiselect("Select 2-5 Cuisines", all_c, default=all_c[:3] if len(all_c) >= 3 else all_c, max_selections=5, key="cmp_cuisine")
        if len(sel_cuisines) >= 2:
            c_data = get_cuisine_radar_data(df_exp, sel_cuisines)
            if len(c_data) >= 2:
                cats = ["Rating", "Affordability", "Speed", "Popularity", "Variety"]
                fig = go.Figure()
                for _, row in c_data.iterrows():
                    fig.add_trace(go.Scatterpolar(r=[row["Avg_Rating_norm"], row["Avg_Cost_norm"], row["Avg_Delivery_norm"], row["Avg_Votes_norm"], row["Restaurant_Count_norm"]], theta=cats, fill='toself', name=row["Cuisine"], line=dict(width=2)))
                fig.update_layout(polar=dict(bgcolor="rgba(255,255,255,0.02)", radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"), angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")), **DARK_LAYOUT, height=480, margin=dict(t=40), legend=dict(font=dict(color="#aaa")))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('<div class="section-header">Cuisine Stats Breakdown</div>', unsafe_allow_html=True)
                st.dataframe(c_data[["Cuisine", "Avg_Rating", "Avg_Cost", "Avg_Delivery", "Restaurant_Count", "Avg_Votes"]].rename(columns={"Avg_Rating": "Rating", "Avg_Cost": "Avg Cost", "Avg_Delivery": "Delivery (min)", "Restaurant_Count": "Restaurants", "Avg_Votes": "Avg Votes"}).style.background_gradient(subset=["Rating"], cmap="viridis").format({"Rating": "{:.2f}", "Avg Cost": "Rs.{:.0f}", "Delivery (min)": "{:.1f}", "Avg Votes": "{:.0f}"}), use_container_width=True, hide_index=True)
    with tab_comp:
        st.markdown('<div class="section-header">Cuisine Competition Heatmap</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight-box">Saturation Index (0-100): higher = more saturated market for that cuisine in that city.</div>', unsafe_allow_html=True)
        comp = get_cuisine_competition(df_exploded, top_cuisines=10)
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.heatmap(comp, annot=True, fmt=".0f", cmap="magma", linewidths=1, linecolor="#1A1A2E", ax=ax, cbar_kws={"shrink": 0.8, "label": "Saturation %"}, annot_kws={"color": "white", "fontsize": 10})
        ax.set_xlabel("City", fontsize=12); ax.set_ylabel("Cuisine", fontsize=12); ax.tick_params(colors="#aaa")
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ---- SECTION 10: CITY BENCHMARKS ----
elif selected_section == "City Benchmarks":
    st.markdown("# City Benchmarks")
    benchmarks = get_city_benchmarks(df_raw)
    render_kpis([
        ("C", f"{len(benchmarks)}", "Cities Analyzed"),
        ("T", benchmarks.iloc[0]["City"] if len(benchmarks) else "-", "Most Restaurants"),
        ("R", f"{benchmarks['Avg_Rating'].max():.2f}" if len(benchmarks) else "-", "Highest Avg Rating"),
        ("D", f"{benchmarks['Avg_Delivery'].min():.0f} min" if len(benchmarks) else "-", "Fastest City"),
    ])
    st.markdown('<div class="section-header">City Comparison Table</div>', unsafe_allow_html=True)
    st.dataframe(benchmarks.style.background_gradient(subset=["Avg_Rating"], cmap="viridis").background_gradient(subset=["Restaurants"], cmap="magma").format({"Avg_Rating": "{:.2f}", "Median_Rating": "{:.2f}", "Avg_Cost": "Rs.{:.0f}", "Median_Cost": "Rs.{:.0f}", "Avg_Delivery": "{:.1f} min", "Min_Delivery": "{:.0f}", "Max_Delivery": "{:.0f}", "Avg_Votes": "{:.0f}", "Total_Votes": "{:,.0f}"}), use_container_width=True, hide_index=True)
    st.download_button("Export City Benchmarks", get_export_csv(benchmarks), "city_benchmarks.csv", "text/csv", key="dl_bench")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">City Radar Comparison</div>', unsafe_allow_html=True)
        cats = ["Rating", "Affordability", "Speed", "Volume", "Areas"]
        fig = go.Figure()
        for _, row in benchmarks.iterrows():
            r_norm = (row["Avg_Rating"] - benchmarks["Avg_Rating"].min()) / max(benchmarks["Avg_Rating"].max() - benchmarks["Avg_Rating"].min(), 0.01)
            c_norm = 1 - (row["Avg_Cost"] - benchmarks["Avg_Cost"].min()) / max(benchmarks["Avg_Cost"].max() - benchmarks["Avg_Cost"].min(), 0.01)
            d_norm = 1 - (row["Avg_Delivery"] - benchmarks["Avg_Delivery"].min()) / max(benchmarks["Avg_Delivery"].max() - benchmarks["Avg_Delivery"].min(), 0.01)
            v_norm = (row["Restaurants"] - benchmarks["Restaurants"].min()) / max(benchmarks["Restaurants"].max() - benchmarks["Restaurants"].min(), 0.01)
            a_norm = (row["Areas"] - benchmarks["Areas"].min()) / max(benchmarks["Areas"].max() - benchmarks["Areas"].min(), 0.01)
            fig.add_trace(go.Scatterpolar(r=[r_norm, c_norm, d_norm, v_norm, a_norm], theta=cats, fill='toself', name=row["City"]))
        fig.update_layout(polar=dict(bgcolor="rgba(255,255,255,0.02)", radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.1)"), angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")), **DARK_LAYOUT, height=450, legend=dict(font=dict(color="#aaa")))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="section-header">Cuisine Diversity Index (Shannon)</div>', unsafe_allow_html=True)
        diversity = get_city_cuisine_diversity(df_exploded)
        fig = px.bar(diversity, x="City", y="Diversity_Index", text="Diversity_Index", color="Unique_Cuisines", color_continuous_scale="Magma", labels={"Diversity_Index": "Shannon Index", "Unique_Cuisines": "Cuisines"})
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(**DARK_LAYOUT, height=450, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box"><b>Shannon Diversity Index</b> measures cuisine variety. Higher = more diverse food scene.</div>', unsafe_allow_html=True)

# ---- SECTION 11: SMART RECOMMENDATIONS ----
elif selected_section == "Smart Recommendations":
    st.markdown("# Smart Recommendations")
    tab_rec, tab_sim = st.tabs(["Personalized Picks", "Find Similar"])
    with tab_rec:
        st.markdown('<div class="section-header">Set Your Preferences</div>', unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            rec_cuisines = ["All"] + sorted(df_exp["Cuisine"].value_counts().head(25).index.tolist())
            rec_cuisine = st.selectbox("Preferred Cuisine", rec_cuisines, key="rec_cuisine")
        with rc2: rec_budget = st.slider("Max Budget (Rs.)", 100, 2000, 600, step=50, key="rec_budget")
        with rc3: rec_delivery = st.slider("Max Delivery (min)", 15, 120, 60, step=5, key="rec_delivery")
        rec_min_rating = st.slider("Min Rating", 0.0, 5.0, 3.5, step=0.1, key="rec_min_r")
        recs = recommend_restaurants(df, cuisine_pref=rec_cuisine, max_cost=rec_budget, min_rating=rec_min_rating, max_delivery=rec_delivery, city=selected_city, top_n=15)
        if len(recs) > 0:
            render_kpis([
                ("M", f"{len(recs)}", "Matches Found"),
                ("T", f"{recs.iloc[0]['Match_Score']:.0f}%", "Top Match"),
                ("R", f"{recs['Rating'].mean():.2f}", "Avg Rating"),
                ("C", f"Rs.{recs['Cost_for_Two'].mean():.0f}", "Avg Cost"),
            ])
            rcols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Delivery_Time", "Cuisine", "Match_Score"]
            st.dataframe(recs[rcols].rename(columns={"Match_Score": "Match %"}).style.background_gradient(subset=["Match %"], cmap="magma").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}", "Delivery_Time": "{:.0f} min", "Match %": "{:.1f}%"}), use_container_width=True, hide_index=True)
            st.download_button("Export Recommendations", get_export_csv(recs, rcols), "recommendations.csv", "text/csv", key="dl_rec")
            st.markdown('<div class="insight-box"><b>Match Score</b> is weighted: Rating (40%) + Affordability (25%) + Speed (20%) + Popularity (15%).</div>', unsafe_allow_html=True)
        else:
            st.warning("No matches found. Try relaxing your preferences.")
    with tab_sim:
        st.markdown('<div class="section-header">Find Restaurants Similar To...</div>', unsafe_allow_html=True)
        all_names = sorted(df["Restaurant"].unique().tolist())
        target = st.selectbox("Select a Restaurant", all_names, key="sim_target")
        if target:
            similar = get_similar_restaurants(df, target, n=10)
            if len(similar) > 0:
                target_row = df[df["Restaurant"] == target].iloc[0]
                st.markdown(f'<div class="insight-box"><b>{target}</b> | Rating: {target_row["Rating"]:.1f} | Cost: Rs.{target_row["Cost_for_Two"]:.0f} | Delivery: {target_row["Delivery_Time"]:.0f} min | {target_row["Area"]}, {target_row["City"]}</div>', unsafe_allow_html=True)
                scols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Delivery_Time", "Cuisine", "Similarity"]
                st.dataframe(similar[scols].rename(columns={"Similarity": "Match %"}).style.background_gradient(subset=["Match %"], cmap="viridis").format({"Rating": "{:.1f}", "Cost_for_Two": "Rs.{:.0f}", "Delivery_Time": "{:.0f} min", "Match %": "{:.1f}%"}), use_container_width=True, hide_index=True)
                st.download_button("Export Similar", get_export_csv(similar, scols), "similar_restaurants.csv", "text/csv", key="dl_sim")
            else:
                st.info("No similar restaurants found.")
