"""
Swiggy Food Delivery Analysis — Utility Functions
Shared data loading, cleaning, and helper functions used by both
the Jupyter Notebook and the Streamlit dashboard.
"""

import pandas as pd
import numpy as np


def load_data(path="data/swiggy.csv"):
    """Load and clean the Swiggy dataset."""
    df = pd.read_csv(path)
    
    # Standardize column names
    df.columns = df.columns.str.strip()
    
    # Rename for consistency
    df = df.rename(columns={
        "Avg ratings": "Rating",
        "Total ratings": "Votes",
        "Delivery time": "Delivery_Time",
        "Price": "Cost_for_Two",
    })
    
    # Clean data types
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
    df["Cost_for_Two"] = pd.to_numeric(df["Cost_for_Two"], errors="coerce")
    df["Delivery_Time"] = pd.to_numeric(df["Delivery_Time"], errors="coerce")
    
    # Drop rows with null ratings
    df = df.dropna(subset=["Rating"])
    
    # Clean cuisine strings — normalize separators
    df["Cuisine"] = df["Cuisine"].fillna("Unknown")
    df["Cuisine"] = df["Cuisine"].str.replace(r"\s{2,}", ",", regex=True)
    
    # Count cuisines per restaurant
    df["Cuisine_Count"] = df["Cuisine"].apply(
        lambda x: len([c.strip() for c in x.split(",") if c.strip()])
    )
    
    # Classify as single vs multi cuisine
    df["Cuisine_Type"] = df["Cuisine_Count"].apply(
        lambda x: "Single" if x == 1 else "Multi"
    )
    
    return df


def explode_cuisines(df):
    """Explode multi-cuisine rows into individual cuisine rows."""
    df_exploded = df.copy()
    df_exploded["Cuisine"] = df_exploded["Cuisine"].str.split(",")
    df_exploded = df_exploded.explode("Cuisine")
    df_exploded["Cuisine"] = df_exploded["Cuisine"].str.strip()
    df_exploded = df_exploded[df_exploded["Cuisine"] != ""]
    return df_exploded


def get_top_cuisines(df_exploded, n=15):
    """Get top N cuisines by restaurant count."""
    return (
        df_exploded.groupby("Cuisine")
        .agg(Count=("Restaurant", "count"), Avg_Rating=("Rating", "mean"))
        .reset_index()
        .sort_values("Count", ascending=False)
        .head(n)
    )


def get_best_rated_cuisines(df_exploded, min_restaurants=100, n=15):
    """Get best-rated cuisines with a minimum restaurant count filter."""
    cuisine_stats = (
        df_exploded.groupby("Cuisine")
        .agg(Count=("Restaurant", "count"), Avg_Rating=("Rating", "mean"))
        .reset_index()
    )
    filtered = cuisine_stats[cuisine_stats["Count"] >= min_restaurants]
    return filtered.sort_values("Avg_Rating", ascending=False).head(n)


def get_location_density(df, top_n=20):
    """Get areas with highest restaurant density."""
    return (
        df.groupby("Area")
        .agg(
            Restaurant_Count=("Restaurant", "count"),
            Avg_Rating=("Rating", "mean"),
            Avg_Cost=("Cost_for_Two", "mean"),
        )
        .reset_index()
        .sort_values("Restaurant_Count", ascending=False)
        .head(top_n)
    )


def get_value_for_money(df, top_n=10):
    """Find best value-for-money restaurants (high rating + low cost)."""
    value_df = df.copy()
    # Normalize rating and cost
    value_df["Rating_Norm"] = (value_df["Rating"] - value_df["Rating"].min()) / (
        value_df["Rating"].max() - value_df["Rating"].min()
    )
    value_df["Cost_Norm"] = (value_df["Cost_for_Two"] - value_df["Cost_for_Two"].min()) / (
        value_df["Cost_for_Two"].max() - value_df["Cost_for_Two"].min()
    )
    # Value Score = High Rating + Low Cost (inverted)
    value_df["Value_Score"] = value_df["Rating_Norm"] + (1 - value_df["Cost_Norm"])
    return value_df.sort_values("Value_Score", ascending=False).head(top_n)


def get_budget_friendly(df, max_cost=300, min_rating=4.0, top_n=10):
    """Top budget-friendly restaurants."""
    budget = df[(df["Cost_for_Two"] <= max_cost) & (df["Rating"] >= min_rating)]
    return budget.sort_values("Rating", ascending=False).head(top_n)


def get_food_hubs(df, min_restaurants=15, min_avg_rating=4.0):
    """Identify food hubs — areas with high density AND high ratings."""
    area_stats = (
        df.groupby("Area")
        .agg(
            Restaurant_Count=("Restaurant", "count"),
            Avg_Rating=("Rating", "mean"),
            Avg_Cost=("Cost_for_Two", "mean"),
            Avg_Delivery=("Delivery_Time", "mean"),
        )
        .reset_index()
    )
    hubs = area_stats[
        (area_stats["Restaurant_Count"] >= min_restaurants)
        & (area_stats["Avg_Rating"] >= min_avg_rating)
    ]
    return hubs.sort_values("Restaurant_Count", ascending=False)


def get_hidden_gems(df, max_votes=100, min_rating=4.5, top_n=15):
    """Hidden gems — low votes but high ratings."""
    gems = df[(df["Votes"] <= max_votes) & (df["Rating"] >= min_rating)]
    return gems.sort_values("Rating", ascending=False).head(top_n)


def get_overhyped(df, min_votes=1000, max_rating=3.5, top_n=15):
    """Overhyped restaurants — high votes but low rating."""
    overhyped = df[(df["Votes"] >= min_votes) & (df["Rating"] <= max_rating)]
    return overhyped.sort_values("Votes", ascending=False).head(top_n)


def get_delivery_by_cuisine(df_exploded, top_n=15):
    """Average delivery time by cuisine."""
    return (
        df_exploded.groupby("Cuisine")
        .agg(
            Avg_Delivery=("Delivery_Time", "mean"),
            Count=("Restaurant", "count"),
        )
        .reset_index()
        .query("Count >= 50")
        .sort_values("Avg_Delivery")
        .head(top_n)
    )


def get_optimal_price_range(df):
    """Find price ranges with highest average ratings."""
    bins = [0, 200, 400, 600, 800, 1000, 1500, 2000]
    labels = ["₹0-200", "₹200-400", "₹400-600", "₹600-800", "₹800-1000", "₹1000-1500", "₹1500+"]
    df_copy = df.copy()
    df_copy["Price_Range"] = pd.cut(df_copy["Cost_for_Two"], bins=bins, labels=labels, right=True)
    return (
        df_copy.groupby("Price_Range", observed=False)
        .agg(
            Avg_Rating=("Rating", "mean"),
            Count=("Restaurant", "count"),
            Avg_Delivery=("Delivery_Time", "mean"),
        )
        .reset_index()
    )


def get_best_location_cuisine_combo(df_exploded, top_n=15):
    """Best location + cuisine combo for opening a new restaurant."""
    combos = (
        df_exploded.groupby(["Area", "Cuisine"])
        .agg(
            Count=("Restaurant", "count"),
            Avg_Rating=("Rating", "mean"),
            Avg_Cost=("Cost_for_Two", "mean"),
        )
        .reset_index()
    )
    combos = combos[combos["Count"] >= 5]
    combos["Score"] = combos["Avg_Rating"] * np.log1p(combos["Count"])
    return combos.sort_values("Score", ascending=False).head(top_n)


# ═══════════════════════════════════════════════════════════════════
# NEW FEATURE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════


def search_restaurants(df, query="", city="All", cuisine_filter="All",
                       min_price=0, max_price=99999, min_rating=0.0,
                       sort_by="Rating", top_n=50):
    """Search and filter restaurants with multiple criteria."""
    result = df.copy()

    if query.strip():
        q = query.strip().lower()
        result = result[
            result["Restaurant"].astype(str).str.lower().str.contains(q, na=False)
            | result["Area"].astype(str).str.lower().str.contains(q, na=False)
            | result["Cuisine"].astype(str).str.lower().str.contains(q, na=False)
        ]

    if city != "All":
        result = result[result["City"] == city]

    if cuisine_filter != "All":
        result = result[result["Cuisine"].str.contains(cuisine_filter, case=False, na=False)]

    result = result[
        (result["Cost_for_Two"] >= min_price)
        & (result["Cost_for_Two"] <= max_price)
        & (result["Rating"] >= min_rating)
    ]

    if sort_by == "Rating":
        result = result.sort_values("Rating", ascending=False)
    elif sort_by == "Cost (Low to High)":
        result = result.sort_values("Cost_for_Two", ascending=True)
    elif sort_by == "Cost (High to Low)":
        result = result.sort_values("Cost_for_Two", ascending=False)
    elif sort_by == "Delivery Time":
        result = result.sort_values("Delivery_Time", ascending=True)
    elif sort_by == "Popularity (Votes)":
        result = result.sort_values("Votes", ascending=False)

    return result.head(top_n)


def get_restaurant_comparison_data(df, restaurant_names):
    """Get normalized data for comparing restaurants with a radar chart."""
    selected = df[df["Restaurant"].isin(restaurant_names)].copy()
    if len(selected) == 0:
        return pd.DataFrame()

    # For multi-row matches (same name), take the best-rated one
    selected = selected.sort_values("Rating", ascending=False).drop_duplicates(
        subset=["Restaurant"], keep="first"
    )

    metrics = ["Rating", "Cost_for_Two", "Delivery_Time", "Votes"]
    for m in metrics:
        col_min = df[m].min()
        col_max = df[m].max()
        if col_max - col_min > 0:
            selected[f"{m}_norm"] = (selected[m] - col_min) / (col_max - col_min)
        else:
            selected[f"{m}_norm"] = 0.5

    # Invert delivery time and cost so higher = better
    selected["Delivery_Time_norm"] = 1 - selected["Delivery_Time_norm"]
    selected["Cost_for_Two_norm"] = 1 - selected["Cost_for_Two_norm"]

    return selected


def get_cuisine_radar_data(df_exp, cuisines):
    """Get multi-dimensional stats for cuisine comparison radar chart."""
    filtered = df_exp[df_exp["Cuisine"].isin(cuisines)]
    stats = (
        filtered.groupby("Cuisine")
        .agg(
            Avg_Rating=("Rating", "mean"),
            Avg_Cost=("Cost_for_Two", "mean"),
            Avg_Delivery=("Delivery_Time", "mean"),
            Restaurant_Count=("Restaurant", "count"),
            Avg_Votes=("Votes", "mean"),
        )
        .reset_index()
    )

    # Normalize each metric 0-1 for radar
    for col in ["Avg_Rating", "Avg_Cost", "Avg_Delivery", "Restaurant_Count", "Avg_Votes"]:
        col_min = stats[col].min()
        col_max = stats[col].max()
        if col_max - col_min > 0:
            stats[f"{col}_norm"] = (stats[col] - col_min) / (col_max - col_min)
        else:
            stats[f"{col}_norm"] = 0.5

    # Invert delivery and cost so higher = better
    stats["Avg_Delivery_norm"] = 1 - stats["Avg_Delivery_norm"]
    stats["Avg_Cost_norm"] = 1 - stats["Avg_Cost_norm"]

    return stats


def get_cuisine_competition(df_exp, top_cuisines=10, top_cities=None):
    """Calculate cuisine competition (saturation) index per city."""
    if top_cities is None:
        top_cities = df_exp["City"].value_counts().head(8).index.tolist()
    top_c = df_exp.groupby("Cuisine").size().nlargest(top_cuisines).index.tolist()

    filtered = df_exp[df_exp["Cuisine"].isin(top_c) & df_exp["City"].isin(top_cities)]
    pivot = filtered.pivot_table(
        index="Cuisine", columns="City", values="Restaurant", aggfunc="count", fill_value=0
    )

    # Normalize to get saturation index per column
    for col in pivot.columns:
        col_max = pivot[col].max()
        if col_max > 0:
            pivot[col] = (pivot[col] / col_max * 100).round(1)

    return pivot


def get_city_benchmarks(df):
    """Get comprehensive city-level benchmark metrics."""
    benchmarks = (
        df.groupby("City")
        .agg(
            Restaurants=("Restaurant", "count"),
            Avg_Rating=("Rating", "mean"),
            Median_Rating=("Rating", "median"),
            Avg_Cost=("Cost_for_Two", "mean"),
            Median_Cost=("Cost_for_Two", "median"),
            Avg_Delivery=("Delivery_Time", "mean"),
            Min_Delivery=("Delivery_Time", "min"),
            Max_Delivery=("Delivery_Time", "max"),
            Avg_Votes=("Votes", "mean"),
            Total_Votes=("Votes", "sum"),
            Areas=("Area", "nunique"),
        )
        .reset_index()
    )
    benchmarks = benchmarks.round(2)
    return benchmarks.sort_values("Restaurants", ascending=False)


def get_city_cuisine_diversity(df_exp):
    """Calculate Shannon diversity index for cuisine variety per city."""
    city_cuisine = (
        df_exp.groupby(["City", "Cuisine"]).size().reset_index(name="Count")
    )
    city_totals = city_cuisine.groupby("City")["Count"].sum().reset_index(name="Total")
    merged = city_cuisine.merge(city_totals, on="City")
    merged["Proportion"] = merged["Count"] / merged["Total"]
    merged["Shannon"] = -merged["Proportion"] * np.log(merged["Proportion"])

    diversity = merged.groupby("City").agg(
        Diversity_Index=("Shannon", "sum"),
        Unique_Cuisines=("Cuisine", "nunique"),
        Total_Restaurants=("Total", "first"),
    ).reset_index().round(3)

    return diversity.sort_values("Diversity_Index", ascending=False)


def recommend_restaurants(df, cuisine_pref="All", max_cost=99999,
                          min_rating=0.0, max_delivery=120,
                          city="All", top_n=15):
    """Score and recommend restaurants based on user preferences."""
    result = df.copy()

    if city != "All":
        result = result[result["City"] == city]

    if cuisine_pref != "All":
        result = result[result["Cuisine"].str.contains(cuisine_pref, case=False, na=False)]

    result = result[
        (result["Cost_for_Two"] <= max_cost)
        & (result["Rating"] >= min_rating)
        & (result["Delivery_Time"] <= max_delivery)
    ]

    if len(result) == 0:
        return result

    # Weighted scoring
    r_min, r_max = result["Rating"].min(), result["Rating"].max()
    c_min, c_max = result["Cost_for_Two"].min(), result["Cost_for_Two"].max()
    d_min, d_max = result["Delivery_Time"].min(), result["Delivery_Time"].max()
    v_min, v_max = result["Votes"].min(), result["Votes"].max()

    def safe_norm(val, vmin, vmax):
        return (val - vmin) / (vmax - vmin) if vmax > vmin else 0.5

    result["Rating_Score"] = result["Rating"].apply(lambda x: safe_norm(x, r_min, r_max))
    result["Cost_Score"] = result["Cost_for_Two"].apply(lambda x: 1 - safe_norm(x, c_min, c_max))
    result["Delivery_Score"] = result["Delivery_Time"].apply(lambda x: 1 - safe_norm(x, d_min, d_max))
    result["Popularity_Score"] = result["Votes"].apply(lambda x: safe_norm(x, v_min, v_max))

    # Weighted match score
    result["Match_Score"] = (
        result["Rating_Score"] * 0.40
        + result["Cost_Score"] * 0.25
        + result["Delivery_Score"] * 0.20
        + result["Popularity_Score"] * 0.15
    )
    result["Match_Score"] = (result["Match_Score"] * 100).round(1)

    return result.sort_values("Match_Score", ascending=False).head(top_n)


def get_similar_restaurants(df, restaurant_name, n=10):
    """Find restaurants similar to a given restaurant based on features."""
    target = df[df["Restaurant"] == restaurant_name]
    if len(target) == 0:
        return pd.DataFrame()

    target = target.iloc[0]
    others = df[df["Restaurant"] != restaurant_name].copy()

    if len(others) == 0:
        return others

    # Compute similarity based on rating, cost, delivery
    r_range = df["Rating"].max() - df["Rating"].min()
    c_range = df["Cost_for_Two"].max() - df["Cost_for_Two"].min()
    d_range = df["Delivery_Time"].max() - df["Delivery_Time"].min()

    def dist(row):
        r_diff = abs(row["Rating"] - target["Rating"]) / (r_range if r_range else 1)
        c_diff = abs(row["Cost_for_Two"] - target["Cost_for_Two"]) / (c_range if c_range else 1)
        d_diff = abs(row["Delivery_Time"] - target["Delivery_Time"]) / (d_range if d_range else 1)

        # Cuisine overlap bonus
        t_cuisines = set(str(target["Cuisine"]).lower().split(","))
        r_cuisines = set(str(row["Cuisine"]).lower().split(","))
        overlap = len(t_cuisines & r_cuisines) / max(len(t_cuisines | r_cuisines), 1)
        cuisine_diff = 1 - overlap

        return r_diff * 0.3 + c_diff * 0.25 + d_diff * 0.15 + cuisine_diff * 0.3

    others["Similarity_Dist"] = others.apply(dist, axis=1)
    others["Similarity"] = ((1 - others["Similarity_Dist"]) * 100).round(1)
    return others.sort_values("Similarity", ascending=False).head(n)


def get_export_csv(df, columns=None):
    """Convert a DataFrame (or a subset of its columns) to CSV bytes for download."""
    if columns:
        df = df[[c for c in columns if c in df.columns]]
    return df.to_csv(index=False).encode("utf-8")
