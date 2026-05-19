"""
Netflix Content Analysis - EDA Script
======================================
Author  : Shital Sarode
Dataset : Netflix Movies and TV Shows (Kaggle)
Purpose : Exploratory Data Analysis on 8,800+ Netflix titles

Run:
    python netflix_analysis.py
"""

import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import sqlite3

warnings.filterwarnings("ignore")

# ── Config ─────────────────────────────────────────────────────────────────
DATA_PATH   = "data/netflix_titles.csv"
CLEAN_PATH  = "data/netflix_cleaned.csv"
VIZ_DIR     = "visualizations"
PALETTE     = {"Movie": "#E50914", "TV Show": "#F5822A"}
BG_COLOR    = "#FAFAFA"

os.makedirs(VIZ_DIR, exist_ok=True)

# ── Matplotlib style ────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor":   BG_COLOR,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})


# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD & INSPECT
# ══════════════════════════════════════════════════════════════════════════════
def load_data(path: str) -> pd.DataFrame:
    print("\n" + "="*60)
    print("  NETFLIX EDA — LOADING DATA")
    print("="*60)

    df = pd.read_csv(path)
    print(f"\n✅ Loaded {len(df):,} rows × {df.shape[1]} columns")
    print(f"\n📋 Columns:\n{list(df.columns)}")
    print(f"\n🔍 Data types:\n{df.dtypes}")
    print(f"\n❓ Missing values:\n{df.isnull().sum()}")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# 2. CLEAN
# ══════════════════════════════════════════════════════════════════════════════
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "="*60)
    print("  DATA CLEANING")
    print("="*60)

    original_rows = len(df)

    # Drop exact duplicates
    df = df.drop_duplicates(subset=["title", "type"], keep="first")

    # Fill missing values
    df["director"]    = df["director"].fillna("Unknown")
    df["cast"]        = df["cast"].fillna("Unknown")
    df["country"]     = df["country"].fillna("Unknown")
    df["rating"]      = df["rating"].fillna("Not Rated")
    df["duration"]    = df["duration"].fillna("Unknown")

    # Drop rows where date_added is missing (needed for time analysis)
    df = df.dropna(subset=["date_added"])

    # Parse date_added
    df["date_added"]  = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
    df["year_added"]  = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month_name()
    df["month_num"]   = df["date_added"].dt.month

    # Duration: split into numeric + unit
    df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)
    df["duration_unit"]  = df["duration"].str.extract(r"([A-Za-z]+.*)")

    # release_year to int
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

    print(f"  Rows before cleaning : {original_rows:,}")
    print(f"  Rows after  cleaning : {len(df):,}")
    print(f"  Rows removed         : {original_rows - len(df):,}")

    df.to_csv(CLEAN_PATH, index=False)
    print(f"\n✅ Cleaned data saved → {CLEAN_PATH}")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# 3. EDA FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def plot_content_type_split(df: pd.DataFrame):
    """Donut chart — Movies vs TV Shows."""
    counts = df["type"].value_counts()
    colors = [PALETTE.get(t, "#888") for t in counts.index]

    fig, ax = plt.subplots(figsize=(6, 6), facecolor=BG_COLOR)
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
        textprops={"fontsize": 13},
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title("Movies vs TV Shows", pad=20, fontsize=16, fontweight="bold")

    # Centre annotation
    ax.text(0, 0, f"{len(df):,}\nTitles", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#333")

    plt.tight_layout()
    path = f"{VIZ_DIR}/01_content_type_split.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_yearly_additions(df: pd.DataFrame):
    """Stacked bar — content added per year."""
    yearly = (
        df[df["year_added"].between(2015, 2021)]
        .groupby(["year_added", "type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    yearly["year_added"] = yearly["year_added"].astype(int)

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG_COLOR)
    x = range(len(yearly))
    movie_col = "Movie" if "Movie" in yearly.columns else yearly.columns[1]
    tv_col    = "TV Show" if "TV Show" in yearly.columns else yearly.columns[2]

    bars_m = ax.bar(x, yearly[movie_col], color=PALETTE["Movie"],    label="Movies",   width=0.55)
    bars_t = ax.bar(x, yearly[tv_col],    color=PALETTE["TV Show"],  label="TV Shows", width=0.55,
                    bottom=yearly[movie_col])

    ax.set_xticks(list(x))
    ax.set_xticklabels(yearly["year_added"].tolist())
    ax.set_xlabel("Year added to Netflix")
    ax.set_ylabel("Number of titles")
    ax.set_title("Content Added to Netflix per Year (2015–2021)")
    ax.legend(frameon=False)

    # value labels on bars
    for bar in bars_m:
        h = bar.get_height()
        if h > 50:
            ax.text(bar.get_x() + bar.get_width()/2, h/2, str(int(h)),
                    ha="center", va="center", fontsize=9, color="white", fontweight="bold")

    plt.tight_layout()
    path = f"{VIZ_DIR}/02_yearly_additions.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_top_genres(df: pd.DataFrame):
    """Horizontal bar — top 10 genres."""
    genres = (
        df["listed_in"]
        .str.split(", ")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG_COLOR)
    colors = [plt.cm.Reds_r(i / len(genres)) for i in range(len(genres))]
    bars = ax.barh(genres.index[::-1], genres.values[::-1], color=colors[::-1], height=0.65)

    for bar, val in zip(bars, genres.values[::-1]):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
                f"{val:,}", va="center", fontsize=10)

    ax.set_xlabel("Number of titles")
    ax.set_title("Top 10 Genres on Netflix")
    ax.set_xlim(0, genres.max() * 1.18)
    plt.tight_layout()
    path = f"{VIZ_DIR}/03_top_genres.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_top_countries(df: pd.DataFrame):
    """Horizontal bar — top 10 producing countries."""
    countries = (
        df[df["country"] != "Unknown"]["country"]
        .str.split(", ")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG_COLOR)
    ax.barh(countries.index[::-1], countries.values[::-1],
            color="#378ADD", height=0.65)

    for i, (idx, val) in enumerate(zip(countries.index[::-1], countries.values[::-1])):
        ax.text(val + 30, i, f"{val:,}", va="center", fontsize=10)

    ax.set_xlabel("Number of titles")
    ax.set_title("Top 10 Content-Producing Countries")
    ax.set_xlim(0, countries.max() * 1.18)
    plt.tight_layout()
    path = f"{VIZ_DIR}/04_top_countries.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_rating_distribution(df: pd.DataFrame):
    """Bar chart — content rating distribution."""
    valid_ratings = ["G","PG","PG-13","R","NC-17","TV-Y","TV-Y7","TV-G","TV-PG","TV-14","TV-MA","NR","UR"]
    ratings = df[df["rating"].isin(valid_ratings)]["rating"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 4), facecolor=BG_COLOR)
    bar_colors = ["#E50914" if r == ratings.idxmax() else "#F5822A" for r in ratings.index]
    ax.bar(ratings.index, ratings.values, color=bar_colors, width=0.6, edgecolor="white")

    for i, (idx, val) in enumerate(ratings.items()):
        ax.text(i, val + 30, str(val), ha="center", fontsize=9, fontweight="bold")

    ax.set_xlabel("Content Rating")
    ax.set_ylabel("Number of Titles")
    ax.set_title("Content Rating Distribution")

    legend_patches = [
        mpatches.Patch(color="#E50914", label="Most common"),
        mpatches.Patch(color="#F5822A", label="Others"),
    ]
    ax.legend(handles=legend_patches, frameon=False)
    plt.tight_layout()
    path = f"{VIZ_DIR}/05_rating_distribution.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_monthly_additions(df: pd.DataFrame):
    """Line chart — average monthly additions."""
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    monthly = (
        df.groupby(["year_added", "month_added"])
        .size()
        .reset_index(name="count")
        .groupby("month_added")["count"]
        .mean()
        .reindex(month_order)
    )

    fig, ax = plt.subplots(figsize=(11, 4), facecolor=BG_COLOR)
    ax.plot(month_order, monthly.values, color="#E50914", linewidth=2.5, marker="o",
            markersize=7, markerfacecolor="white", markeredgewidth=2)
    ax.fill_between(month_order, monthly.values, alpha=0.08, color="#E50914")

    peak_month = monthly.idxmax()
    ax.annotate(f"Peak: {peak_month}", xy=(list(month_order).index(peak_month), monthly[peak_month]),
                xytext=(0, 20), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#555"), fontsize=10, color="#E50914")

    ax.set_xticklabels([m[:3] for m in month_order])
    ax.set_ylabel("Avg. titles added")
    ax.set_title("Average Monthly Content Additions")
    plt.tight_layout()
    path = f"{VIZ_DIR}/06_monthly_additions.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_top_directors(df: pd.DataFrame):
    """Bar chart — top 10 directors."""
    directors = (
        df[df["director"] != "Unknown"]["director"]
        .str.split(", ")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG_COLOR)
    ax.barh(directors.index[::-1], directors.values[::-1], color="#6C5CE7", height=0.65)

    for i, val in enumerate(directors.values[::-1]):
        ax.text(val + 0.3, i, str(val), va="center", fontsize=10)

    ax.set_xlabel("Number of titles directed")
    ax.set_title("Top 10 Directors on Netflix")
    ax.set_xlim(0, directors.max() * 1.2)
    plt.tight_layout()
    path = f"{VIZ_DIR}/07_top_directors.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


def plot_movie_duration(df: pd.DataFrame):
    """Histogram — movie duration distribution."""
    movies = df[(df["type"] == "Movie") & df["duration_value"].notna()]

    fig, ax = plt.subplots(figsize=(9, 4), facecolor=BG_COLOR)
    ax.hist(movies["duration_value"], bins=40, color="#E50914", edgecolor="white", alpha=0.85)
    ax.axvline(movies["duration_value"].median(), color="#333", linestyle="--", linewidth=1.5,
               label=f"Median: {int(movies['duration_value'].median())} min")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of movies")
    ax.set_title("Movie Duration Distribution")
    ax.legend(frameon=False)
    plt.tight_layout()
    path = f"{VIZ_DIR}/08_movie_duration.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. SQL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def run_sql_analysis(df: pd.DataFrame):
    print("\n" + "="*60)
    print("  SQL ANALYSIS (SQLite in-memory)")
    print("="*60)

    conn = sqlite3.connect(":memory:")
    df.to_sql("netflix", conn, index=False, if_exists="replace")

    queries = {
        "Total titles by type": """
            SELECT type, COUNT(*) AS total
            FROM netflix
            GROUP BY type
            ORDER BY total DESC;
        """,
        "Top 5 countries by content": """
            SELECT country, COUNT(*) AS total
            FROM netflix
            WHERE country != 'Unknown'
            GROUP BY country
            ORDER BY total DESC
            LIMIT 5;
        """,
        "Content added per year (2016-2021)": """
            SELECT year_added, COUNT(*) AS titles_added
            FROM netflix
            WHERE year_added BETWEEN 2016 AND 2021
            GROUP BY year_added
            ORDER BY year_added;
        """,
        "Top 5 ratings": """
            SELECT rating, COUNT(*) AS count
            FROM netflix
            WHERE rating NOT IN ('Unknown', 'Not Rated')
            GROUP BY rating
            ORDER BY count DESC
            LIMIT 5;
        """,
        "Average movie duration (min)": """
            SELECT ROUND(AVG(duration_value), 1) AS avg_duration_minutes
            FROM netflix
            WHERE type = 'Movie' AND duration_value IS NOT NULL;
        """,
        "Top 5 directors": """
            SELECT director, COUNT(*) AS titles
            FROM netflix
            WHERE director != 'Unknown'
            GROUP BY director
            ORDER BY titles DESC
            LIMIT 5;
        """,
    }

    for title, query in queries.items():
        print(f"\n📊 {title}")
        print("-" * 40)
        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))

    conn.close()


# ══════════════════════════════════════════════════════════════════════════════
# 5. SUMMARY STATS
# ══════════════════════════════════════════════════════════════════════════════
def print_summary(df: pd.DataFrame):
    print("\n" + "="*60)
    print("  SUMMARY STATISTICS")
    print("="*60)

    movies = df[df["type"] == "Movie"]
    tv     = df[df["type"] == "TV Show"]

    print(f"\n  Total titles       : {len(df):,}")
    print(f"  Movies             : {len(movies):,} ({len(movies)/len(df)*100:.1f}%)")
    print(f"  TV Shows           : {len(tv):,}    ({len(tv)/len(df)*100:.1f}%)")
    print(f"  Unique countries   : {df['country'].nunique():,}")
    print(f"  Year range         : {int(df['release_year'].min())} – {int(df['release_year'].max())}")
    print(f"  Avg. movie duration: {movies['duration_value'].mean():.0f} min")
    print(f"  Most common rating : {df['rating'].value_counts().idxmax()}")
    print(f"  Top genre          : {df['listed_in'].str.split(', ').explode().value_counts().idxmax()}")
    print(f"  Top country        : {df[df['country']!='Unknown']['country'].str.split(', ').explode().value_counts().idxmax()}")


# ══════════════════════════════════════════════════════════════════════════════
# 6. MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    if not os.path.exists(DATA_PATH):
        print(f"\n❌ Dataset not found at '{DATA_PATH}'")
        print("   Download from: https://www.kaggle.com/datasets/shivamb/netflix-shows")
        print("   Place 'netflix_titles.csv' inside the 'data/' folder.")
        return

    df = load_data(DATA_PATH)
    df = clean_data(df)
    print_summary(df)

    print("\n" + "="*60)
    print("  GENERATING VISUALIZATIONS")
    print("="*60)
    plot_content_type_split(df)
    plot_yearly_additions(df)
    plot_top_genres(df)
    plot_top_countries(df)
    plot_rating_distribution(df)
    plot_monthly_additions(df)
    plot_top_directors(df)
    plot_movie_duration(df)

    run_sql_analysis(df)

    print("\n" + "="*60)
    print("  ✅ ANALYSIS COMPLETE")
    print(f"  All charts saved in: ./{VIZ_DIR}/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
