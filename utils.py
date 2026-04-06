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
