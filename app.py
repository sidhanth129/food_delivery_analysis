"""
🍔 Swiggy Food Delivery Analysis — Interactive Dashboard
Built with Streamlit, Seaborn & Matplotlib
Light Theme Edition
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data, explode_cuisines, get_top_cuisines, get_best_rated_cuisines,
    get_location_density, get_value_for_money, get_budget_friendly,
    get_food_hubs, get_hidden_gems, get_overhyped, get_delivery_by_cuisine,
    get_optimal_price_range, get_best_location_cuisine_combo,
)

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="🍔 Swiggy Food Delivery Analysis",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS (Light Theme) ──────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    *, html, body, [class*="st-"] { font-family: 'Inter', sans-serif !important; }
    
    .main { background: #F8F9FA; }
    
    /* ─── KPI Cards ─── */
    .kpi-row {
        display: flex;
        gap: 16px;
        margin: 16px 0 28px;
    }
    .kpi-card {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E8ECF1;
        border-radius: 14px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        min-width: 0;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    }
    .kpi-icon { font-size: 1.6rem; margin-bottom: 4px; }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FF4B4B;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #7A8599;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-top: 6px;
    }
    
    /* ─── Section Headers ─── */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1E1E1E;
        margin: 28px 0 14px;
        padding-bottom: 8px;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #FF4B4B, #FF8E53, transparent) 1;
    }
    
    /* ─── Insight Box ─── */
    .insight-box {
        background: #FFF5F5;
        border-left: 4px solid #FF4B4B;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 12px 0;
        color: #333;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    
    /* ─── Sidebar ─── */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FA 100%);
        border-right: 1px solid #E8ECF1;
    }
    div[data-testid="stSidebar"] .stMarkdown h2 { color: #1E1E1E !important; }
    
    h1 { color: #1E1E1E !important; font-weight: 800 !important; }
    h2, h3 { color: #2D3748 !important; }
    
    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
        font-weight: 600;
    }
    
    /* ─── Dataframes ─── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Data Loading ───────────────────────────────────────────────
@st.cache_data
def get_data():
    df = load_data()
    df_exp = explode_cuisines(df)
    return df, df_exp


df_raw, df_exploded = get_data()

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍔 Swiggy Analysis")
    st.markdown("---")
    
    cities = ["All"] + sorted(df_raw["City"].unique().tolist())
    selected_city = st.selectbox("🏙️ Select City", cities, index=0)
    
    st.markdown("---")
    
    sections = [
        "🏠 Overview",
        "🍽️ Cuisine Analysis",
        "📍 Location Intelligence",
        "💰 Value Analysis",
        "⏱️ Delivery Performance",
        "🔍 Hidden Gems & Overhyped",
        "📊 Business Insights",
    ]
    selected_section = st.radio("📑 Navigate", sections, index=0)
    
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit · Data: Swiggy")

# ─── Filter Data ────────────────────────────────────────────────
if selected_city != "All":
    df = df_raw[df_raw["City"] == selected_city].copy()
    df_exp = df_exploded[df_exploded["City"] == selected_city].copy()
else:
    df = df_raw.copy()
    df_exp = df_exploded.copy()


# ─── Light Plot Style ───────────────────────────────────────────
def set_plot_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FAFBFC",
        "axes.edgecolor": "#DEE2E6",
        "axes.labelcolor": "#333333",
        "xtick.color": "#555555",
        "ytick.color": "#555555",
        "text.color": "#333333",
        "grid.color": "#EDF0F3",
        "grid.alpha": 0.7,
        "font.family": "sans-serif",
        "font.size": 11,
    })


PALETTE = ["#FF4B4B", "#FF8E53", "#FFC857", "#36D7B7", "#3B82F6",
           "#8B5CF6", "#EC4899", "#F59E0B", "#10B981", "#6366F1",
           "#14B8A6", "#F97316", "#A855F7", "#0EA5E9", "#EF4444"]

set_plot_style()


# ─── Helper: render KPI row ─────────────────────────────────────
def render_kpis(items):
    """items = list of (icon, value, label) tuples"""
    cards = ""
    for icon, value, label in items:
        cards += f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>"""
    st.markdown(f'<div class="kpi-row">{cards}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════
if selected_section == "🏠 Overview":
    st.markdown("# 🍔 Swiggy Food Delivery Analysis")
    city_label = selected_city if selected_city != "All" else f"{df['City'].nunique()} cities"
    st.markdown(f"*Analyzing **{len(df):,}** restaurants across **{city_label}***")
    
    # KPI Cards
    render_kpis([
        ("🏪", f"{len(df):,}", "Total Restaurants"),
        ("⭐", f"{df['Rating'].mean():.2f}", "Avg Rating"),
        ("💰", f"₹{df['Cost_for_Two'].mean():.0f}", "Avg Cost for Two"),
        ("⏱️", f"{df['Delivery_Time'].mean():.0f} min", "Avg Delivery Time"),
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">City Distribution</div>', unsafe_allow_html=True)
        city_counts = df["City"].value_counts()
        fig = px.pie(
            values=city_counts.values, names=city_counts.index, hole=0.5,
            color_discrete_sequence=PALETTE,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333", size=12), height=420, margin=dict(t=10, b=10),
            legend=dict(font=dict(size=11)),
        )
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Rating Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5.2))
        sns.histplot(df["Rating"], bins=20, kde=True, color="#FF4B4B", ax=ax, edgecolor="white", alpha=0.8)
        ax.axvline(df["Rating"].mean(), color="#3B82F6", linestyle="--", linewidth=2,
                   label=f"Mean: {df['Rating'].mean():.2f}")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        ax.legend(fontsize=11, frameon=True, facecolor="white")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Top Areas
    st.markdown('<div class="section-header">Top 10 Areas by Restaurant Count</div>', unsafe_allow_html=True)
    top_areas = df["Area"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.barh(top_areas.index[::-1], top_areas.values[::-1],
                   color=PALETTE[:10], edgecolor="white", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{int(bar.get_width())}', va='center', fontsize=11, color="#333", fontweight="bold")
    ax.set_xlabel("Number of Restaurants")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════════
# SECTION 2: CUISINE ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif selected_section == "🍽️ Cuisine Analysis":
    st.markdown("# 🍽️ Cuisine Analysis")
    
    render_kpis([
        ("🍕", f"{df_exp['Cuisine'].nunique()}", "Unique Cuisines"),
        ("🏆", f"{df_exp.groupby('Cuisine').size().idxmax()}", "Most Popular"),
        ("📊", f"{df['Cuisine_Type'].value_counts().get('Multi', 0):,}", "Multi-Cuisine"),
        ("🍛", f"{df['Cuisine_Type'].value_counts().get('Single', 0):,}", "Single-Cuisine"),
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Top 15 Most Popular Cuisines</div>', unsafe_allow_html=True)
        top_cuisines = get_top_cuisines(df_exp, 15)
        fig, ax = plt.subplots(figsize=(8, 7))
        bars = ax.barh(top_cuisines["Cuisine"].values[::-1], top_cuisines["Count"].values[::-1],
                       color=PALETTE[:15][::-1], edgecolor="white", height=0.7)
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'{int(bar.get_width())}', va='center', fontsize=10, color="#333", fontweight="bold")
        ax.set_xlabel("Number of Restaurants")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown('<div class="section-header">Best Rated Cuisines (100+ restaurants)</div>', unsafe_allow_html=True)
        best_rated = get_best_rated_cuisines(df_exp, min_restaurants=100, n=15)
        if len(best_rated) > 0:
            fig, ax = plt.subplots(figsize=(8, 7))
            colors = [PALETTE[i % len(PALETTE)] for i in range(len(best_rated))]
            bars = ax.barh(best_rated["Cuisine"].values[::-1], best_rated["Avg_Rating"].values[::-1],
                           color=colors[::-1], edgecolor="white", height=0.7)
            for bar in bars:
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{bar.get_width():.2f}', va='center', fontsize=10, color="#333", fontweight="bold")
            ax.set_xlabel("Average Rating")
            ax.set_xlim(left=3.5)
            ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        else:
            st.info("Not enough data. Try selecting 'All' cities.")
    
    # Cuisine heatmap
    st.markdown('<div class="section-header">Cuisine Popularity Across Cities</div>', unsafe_allow_html=True)
    top_10_cuisines = df_exploded.groupby("Cuisine").size().nlargest(10).index.tolist()
    heatmap_data = df_exploded[df_exploded["Cuisine"].isin(top_10_cuisines)]
    pivot = heatmap_data.pivot_table(index="Cuisine", columns="City", values="Restaurant", aggfunc="count", fill_value=0)
    
    fig, ax = plt.subplots(figsize=(14, 5.5))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd", linewidths=1,
                linecolor="white", ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_xlabel("City", fontsize=12)
    ax.set_ylabel("Cuisine", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Multi vs Single
    st.markdown('<div class="section-header">Multi-Cuisine vs Single-Cuisine Performance</div>', unsafe_allow_html=True)
    cuisine_type_stats = df.groupby("Cuisine_Type").agg(
        Avg_Rating=("Rating", "mean"), Avg_Cost=("Cost_for_Two", "mean"),
        Count=("Restaurant", "count"), Avg_Delivery=("Delivery_Time", "mean"),
    ).reset_index()
    
    c1, c2, c3 = st.columns(3)
    metrics_data = [
        ("Avg Rating", "Avg_Rating", c1, (3.5, 4.5)),
        ("Avg Cost (₹)", "Avg_Cost", c2, None),
        ("Avg Delivery (min)", "Avg_Delivery", c3, None),
    ]
    for title, col, container, ylim in metrics_data:
        with container:
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.bar(cuisine_type_stats["Cuisine_Type"], cuisine_type_stats[col],
                          color=["#FF4B4B", "#36D7B7"], edgecolor="white", width=0.5)
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
                        f'{bar.get_height():.2f}', ha='center', fontsize=12, color="#333", fontweight="bold")
            ax.set_ylabel(title)
            ax.set_title(title, fontsize=13, fontweight="bold", color="#333")
            if ylim: ax.set_ylim(ylim)
            ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()


# ═══════════════════════════════════════════════════════════════
# SECTION 3: LOCATION INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
elif selected_section == "📍 Location Intelligence":
    st.markdown("# 📍 Location Intelligence")
    
    # Density
    st.markdown('<div class="section-header">Top 20 Areas by Restaurant Density</div>', unsafe_allow_html=True)
    density = get_location_density(df, top_n=20)
    fig = px.bar(density, x="Area", y="Restaurant_Count", color="Avg_Rating",
                 color_continuous_scale="RdYlGn", text="Restaurant_Count",
                 labels={"Restaurant_Count": "Restaurants", "Avg_Rating": "Avg Rating"})
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#333"), height=450, margin=dict(t=20),
        xaxis=dict(tickangle=-45),
    )
    fig.update_traces(textposition="outside", textfont_size=10)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Cost Variation Across Top Areas</div>', unsafe_allow_html=True)
        top_areas = df["Area"].value_counts().head(10).index.tolist()
        df_top = df[df["Area"].isin(top_areas)]
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df_top, x="Area", y="Cost_for_Two", palette=PALETTE[:10], ax=ax,
                    flierprops=dict(marker="o", markerfacecolor="#FF4B4B", markersize=3, alpha=0.5))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.set_xlabel("")
        ax.set_ylabel("Cost for Two (₹)")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown('<div class="section-header">Rating Distribution per Area</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.violinplot(data=df_top, x="Area", y="Rating", palette=PALETTE[:10], ax=ax, inner="quartile")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.set_xlabel("")
        ax.set_ylabel("Rating")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Food Hubs
    st.markdown('<div class="section-header">🏆 Food Hubs (High Density + High Ratings)</div>', unsafe_allow_html=True)
    hubs = get_food_hubs(df, min_restaurants=10, min_avg_rating=4.0)
    if len(hubs) > 0:
        fig = px.scatter(hubs, x="Restaurant_Count", y="Avg_Rating",
                         size="Avg_Cost", color="Avg_Delivery",
                         text="Area", color_continuous_scale="YlOrRd",
                         labels={"Restaurant_Count": "Restaurants", "Avg_Rating": "Rating",
                                 "Avg_Cost": "Avg Cost ₹", "Avg_Delivery": "Delivery (min)"})
        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333"), height=500, margin=dict(t=20),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">💡 <strong>Food Hubs</strong> = areas with 10+ restaurants AND avg rating ≥ 4.0. Bubble size = avg cost, color = delivery time.</div>', unsafe_allow_html=True)
    else:
        st.info("No food hubs found with current filters.")
    
    # Delivery by area
    st.markdown('<div class="section-header">Fastest Delivery Areas</div>', unsafe_allow_html=True)
    delivery_by_area = (
        df.groupby("Area")["Delivery_Time"].agg(["mean", "count"]).reset_index()
        .query("count >= 10").sort_values("mean")
    )
    top_fast = delivery_by_area.head(15)
    fig, ax = plt.subplots(figsize=(14, 5))
    bars = ax.barh(top_fast["Area"].values[::-1], top_fast["mean"].values[::-1],
                   color="#36D7B7", edgecolor="white", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.1f} min', va='center', fontsize=10, color="#333", fontweight="bold")
    ax.set_xlabel("Avg Delivery Time (min)")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════════
# SECTION 4: VALUE ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif selected_section == "💰 Value Analysis":
    st.markdown("# 💰 Customer Value Analysis")
    
    # Cost vs Rating
    st.markdown('<div class="section-header">Cost vs Rating Correlation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        fig = px.scatter(df, x="Cost_for_Two", y="Rating", color="City",
                         opacity=0.4, size_max=8,
                         color_discrete_sequence=PALETTE,
                         labels={"Cost_for_Two": "Cost for Two (₹)", "Rating": "Rating"},
                         trendline="ols")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333"), height=480, margin=dict(t=20),
            legend=dict(font=dict(size=10)),
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        corr = df["Cost_for_Two"].corr(df["Rating"])
        st.markdown(f"""
        <div class="kpi-card" style="margin-top:40px;">
            <div class="kpi-icon">📈</div>
            <div class="kpi-value">{corr:.3f}</div>
            <div class="kpi-label">Correlation</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if abs(corr) < 0.15:
            st.markdown('<div class="insight-box">💡 <strong>Weak correlation</strong> — Price has negligible impact on ratings. Affordable restaurants can be just as good!</div>', unsafe_allow_html=True)
        elif corr > 0:
            st.markdown('<div class="insight-box">💡 <strong>Positive correlation</strong> — Pricier restaurants tend to rate slightly higher.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="insight-box">💡 <strong>Negative correlation</strong> — Higher price does NOT guarantee better ratings.</div>', unsafe_allow_html=True)
    
    # Value for Money
    st.markdown('<div class="section-header">🏆 Best Value-for-Money Restaurants</div>', unsafe_allow_html=True)
    vfm = get_value_for_money(df, top_n=10)
    display_cols = ["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Cuisine", "Value_Score"]
    st.dataframe(
        vfm[display_cols].style.background_gradient(subset=["Value_Score"], cmap="YlOrRd")
        .format({"Rating": "{:.1f}", "Value_Score": "{:.2f}", "Cost_for_Two": "₹{:.0f}"}),
        use_container_width=True, hide_index=True,
    )
    
    # Budget Friendly
    st.markdown('<div class="section-header">💸 Top 10 Budget-Friendly Restaurants</div>', unsafe_allow_html=True)
    col_cost, col_rating = st.columns(2)
    with col_cost:
        max_cost = st.slider("Max Cost for Two (₹)", 100, 500, 300, step=50)
    with col_rating:
        min_rating = st.slider("Min Rating", 3.0, 5.0, 4.0, step=0.1)
    
    budget = get_budget_friendly(df, max_cost=max_cost, min_rating=min_rating, top_n=10)
    if len(budget) > 0:
        st.dataframe(
            budget[["Restaurant", "Area", "City", "Rating", "Cost_for_Two", "Cuisine", "Delivery_Time"]]
            .style.background_gradient(subset=["Rating"], cmap="Greens")
            .format({"Rating": "{:.1f}", "Cost_for_Two": "₹{:.0f}", "Delivery_Time": "{:.0f} min"}),
            use_container_width=True, hide_index=True,
        )
    else:
        st.warning("No restaurants found with these filters. Try adjusting the sliders.")


# ═══════════════════════════════════════════════════════════════
# SECTION 5: DELIVERY PERFORMANCE
# ═══════════════════════════════════════════════════════════════
elif selected_section == "⏱️ Delivery Performance":
    st.markdown("# ⏱️ Delivery Performance")
    
    render_kpis([
        ("🚀", f"{df['Delivery_Time'].min():.0f} min", "Fastest"),
        ("🐌", f"{df['Delivery_Time'].max():.0f} min", "Slowest"),
        ("📊", f"{df['Delivery_Time'].mean():.1f} min", "Average"),
        ("📏", f"{df['Delivery_Time'].median():.0f} min", "Median"),
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Delivery Time Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df["Delivery_Time"], bins=30, kde=True, color="#3B82F6", ax=ax, edgecolor="white", alpha=0.8)
        ax.axvline(df["Delivery_Time"].mean(), color="#FF4B4B", linestyle="--", linewidth=2,
                   label=f"Mean: {df['Delivery_Time'].mean():.1f} min")
        ax.set_xlabel("Delivery Time (min)")
        ax.set_ylabel("Count")
        ax.legend(fontsize=11, frameon=True, facecolor="white")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown('<div class="section-header">Delivery Time vs Rating</div>', unsafe_allow_html=True)
        fig = px.scatter(df, x="Delivery_Time", y="Rating", opacity=0.2,
                         color_discrete_sequence=["#3B82F6"], trendline="ols",
                         labels={"Delivery_Time": "Delivery Time (min)"})
        corr = df["Delivery_Time"].corr(df["Rating"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333"), height=400, margin=dict(t=20),
            title=f"Correlation: {corr:.3f}",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Fastest cuisines
    st.markdown('<div class="section-header">Fastest Delivery Cuisines (50+ restaurants)</div>', unsafe_allow_html=True)
    fast_cuisines = get_delivery_by_cuisine(df_exp, top_n=15)
    fig, ax = plt.subplots(figsize=(14, 5.5))
    bars = ax.barh(fast_cuisines["Cuisine"].values[::-1], fast_cuisines["Avg_Delivery"].values[::-1],
                   color=PALETTE[:len(fast_cuisines)][::-1], edgecolor="white", height=0.65)
    for bar in bars:
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.1f} min', va='center', fontsize=10, color="#333", fontweight="bold")
    ax.set_xlabel("Avg Delivery Time (min)")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Delivery by City
    st.markdown('<div class="section-header">Delivery Time by City</div>', unsafe_allow_html=True)
    city_delivery = df_raw.groupby("City")["Delivery_Time"].mean().sort_values()
    fig = px.bar(x=city_delivery.index, y=city_delivery.values, text=city_delivery.values,
                 color=city_delivery.values, color_continuous_scale="RdYlGn_r",
                 labels={"x": "City", "y": "Avg Delivery Time (min)"})
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#333"), height=400, margin=dict(t=20), showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 6: HIDDEN GEMS & OVERHYPED
# ═══════════════════════════════════════════════════════════════
elif selected_section == "🔍 Hidden Gems & Overhyped":
    st.markdown("# 🔍 Hidden Gems & Overhyped Restaurants")
    
    tab1, tab2 = st.tabs(["💎 Hidden Gems", "📢 Overhyped"])
    
    with tab1:
        st.markdown('<div class="section-header">💎 Hidden Gems</div>', unsafe_allow_html=True)
        col_v, col_r = st.columns(2)
        with col_v:
            gem_max_votes = st.slider("Max Votes", 20, 500, 100, step=10, key="gem_votes")
        with col_r:
            gem_min_rating = st.slider("Min Rating", 4.0, 5.0, 4.5, step=0.1, key="gem_rating")
        
        gems = get_hidden_gems(df, max_votes=gem_max_votes, min_rating=gem_min_rating, top_n=15)
        if len(gems) > 0:
            st.dataframe(
                gems[["Restaurant", "Area", "City", "Rating", "Votes", "Cost_for_Two", "Cuisine"]]
                .style.background_gradient(subset=["Rating"], cmap="Greens")
                .format({"Rating": "{:.1f}", "Cost_for_Two": "₹{:.0f}"}),
                use_container_width=True, hide_index=True,
            )
            
            fig, ax = plt.subplots(figsize=(14, 5))
            bars = ax.barh(gems["Restaurant"].values[::-1], gems["Rating"].values[::-1],
                           color="#10B981", edgecolor="white", height=0.65)
            for bar, votes in zip(bars, gems["Votes"].values[::-1]):
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{bar.get_width():.1f} ⭐ ({int(votes)} votes)', va='center', fontsize=9, color="#333")
            ax.set_xlabel("Rating")
            ax.set_xlim(left=4.0)
            ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            st.markdown('<div class="insight-box">💡 These restaurants have excellent ratings but haven\'t gained popularity yet. Great picks for adventurous foodies!</div>', unsafe_allow_html=True)
        else:
            st.info("No hidden gems found. Try adjusting the filters.")
    
    with tab2:
        st.markdown('<div class="section-header">📢 Overhyped Restaurants</div>', unsafe_allow_html=True)
        col_v2, col_r2 = st.columns(2)
        with col_v2:
            oh_min_votes = st.slider("Min Votes", 500, 10000, 1000, step=500, key="oh_votes")
        with col_r2:
            oh_max_rating = st.slider("Max Rating", 2.0, 4.0, 3.5, step=0.1, key="oh_rating")
        
        overhyped = get_overhyped(df, min_votes=oh_min_votes, max_rating=oh_max_rating, top_n=15)
        if len(overhyped) > 0:
            st.dataframe(
                overhyped[["Restaurant", "Area", "City", "Rating", "Votes", "Cost_for_Two", "Cuisine"]]
                .style.background_gradient(subset=["Rating"], cmap="Reds_r")
                .format({"Rating": "{:.1f}", "Cost_for_Two": "₹{:.0f}"}),
                use_container_width=True, hide_index=True,
            )
            
            fig = px.scatter(overhyped, x="Votes", y="Rating", size="Cost_for_Two",
                             text="Restaurant", color_discrete_sequence=["#FF4B4B"],
                             labels={"Votes": "Total Votes", "Cost_for_Two": "Cost ₹"})
            fig.update_traces(textposition="top center", textfont_size=9)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#333"), height=450, margin=dict(t=20),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="insight-box">⚠️ These restaurants are widely known but underperform on ratings. High visibility ≠ high quality.</div>', unsafe_allow_html=True)
        else:
            st.info("No overhyped restaurants found. Try adjusting the filters.")


# ═══════════════════════════════════════════════════════════════
# SECTION 7: BUSINESS INSIGHTS
# ═══════════════════════════════════════════════════════════════
elif selected_section == "📊 Business Insights":
    st.markdown("# 📊 Business Insights")
    
    # Optimal Price Range
    st.markdown('<div class="section-header">Optimal Price Range for Highest Ratings</div>', unsafe_allow_html=True)
    price_stats = get_optimal_price_range(df)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(price_stats, x="Price_Range", y="Avg_Rating", text="Avg_Rating",
                     color="Avg_Rating", color_continuous_scale="RdYlGn",
                     labels={"Price_Range": "Price Range", "Avg_Rating": "Avg Rating"})
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333"), height=420, margin=dict(t=20),
            yaxis=dict(range=[3.3, 4.6]), showlegend=False,
            title="Avg Rating by Price Range",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(price_stats, x="Price_Range", y="Count", text="Count",
                     color_discrete_sequence=["#3B82F6"],
                     labels={"Price_Range": "Price Range", "Count": "Restaurants"})
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333"), height=420, margin=dict(t=20),
            title="Restaurant Count by Price Range",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    best_range = price_stats.loc[price_stats["Avg_Rating"].idxmax(), "Price_Range"]
    st.markdown(f'<div class="insight-box">💡 <strong>Optimal Price Range:</strong> Restaurants in the <strong>{best_range}</strong> bracket achieve the highest average rating — the sweet spot for quality and market appeal.</div>', unsafe_allow_html=True)
    
    # Best Combos
    st.markdown('<div class="section-header">Best Location + Cuisine Combos for New Restaurant</div>', unsafe_allow_html=True)
    combos = get_best_location_cuisine_combo(df_exp, top_n=15)
    if len(combos) > 0:
        st.dataframe(
            combos[["Area", "Cuisine", "Count", "Avg_Rating", "Avg_Cost", "Score"]]
            .rename(columns={"Count": "Existing", "Avg_Rating": "Avg Rating",
                             "Avg_Cost": "Avg Cost ₹", "Score": "Opportunity"})
            .style.background_gradient(subset=["Opportunity"], cmap="YlOrRd")
            .format({"Avg Rating": "{:.2f}", "Avg Cost ₹": "₹{:.0f}", "Opportunity": "{:.2f}"}),
            use_container_width=True, hide_index=True,
        )
        st.markdown('<div class="insight-box">💡 <strong>Opportunity Score</strong> = Rating × log(Count). High scores indicate proven demand + quality in that area-cuisine pair.</div>', unsafe_allow_html=True)
    
    # Dominant Cuisines per Area
    st.markdown('<div class="section-header">Dominant Cuisines in Top Areas</div>', unsafe_allow_html=True)
    top_areas = df["Area"].value_counts().head(8).index.tolist()
    df_top_areas = df_exp[df_exp["Area"].isin(top_areas)]
    dominant = (
        df_top_areas.groupby(["Area", "Cuisine"]).size()
        .reset_index(name="Count")
        .sort_values(["Area", "Count"], ascending=[True, False])
    )
    dominant_top = dominant.groupby("Area").head(5).reset_index(drop=True)
    
    fig = px.bar(dominant_top, x="Area", y="Count", color="Cuisine", barmode="group",
                 color_discrete_sequence=PALETTE,
                 labels={"Count": "Restaurants"})
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#333"), height=480, margin=dict(t=20),
        legend=dict(font=dict(size=10)), xaxis=dict(tickangle=-30),
    )
    st.plotly_chart(fig, use_container_width=True)
