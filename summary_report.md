# Netflix EDA — Key Findings Report

**Dataset:** 8,807 Netflix titles (2008–2021)  
**Analysis Date:** 2024  
**Tools:** Python, Pandas, Matplotlib, SQLite

---

## Executive Summary

This report summarizes the findings from an exploratory data analysis of the Netflix content library. The analysis covers content type distribution, temporal trends, genre popularity, country-wise production, content ratings, and director insights.

---

## 1. Content Type Distribution

- The Netflix library consists of **6,131 Movies (69.6%)** and **2,676 TV Shows (30.4%)**
- Movies significantly outnumber TV Shows — nearly 2.3x more movies
- Both categories have grown steadily since 2015

---

## 2. Growth Trends

| Year | Movies | TV Shows | Total |
|------|--------|----------|-------|
| 2015 | 82     | 37       | 119   |
| 2016 | 189    | 75       | 264   |
| 2017 | 381    | 165      | 546   |
| 2018 | 767    | 378      | 1,145 |
| 2019 | 1,030  | 567      | 1,597 |
| 2020 | 890    | 519      | 1,409 |
| 2021 | 410    | 205      | 615   |

**Key insight:** Content additions peaked in **2019**, with over 1,597 titles added. The slight drop in 2020–2021 may reflect COVID-19 production delays.

---

## 3. Genre Analysis

| Rank | Genre | Titles |
|------|-------|--------|
| 1 | Dramas | 2,427 |
| 2 | Comedies | 1,674 |
| 3 | Documentaries | 869 |
| 4 | Action & Adventure | 859 |
| 5 | Thrillers | 782 |
| 6 | Children & Family | 641 |
| 7 | Romantic Movies | 559 |
| 8 | Horror Movies | 357 |
| 9 | Crime TV Shows | 349 |
| 10 | Stand-Up Comedy | 334 |

**Key insight:** Dramas dominate by a large margin. Documentaries rank 3rd, showing Netflix's investment in non-fiction content.

---

## 4. Country Distribution

| Rank | Country | Titles | % of Library |
|------|---------|--------|-------------|
| 1 | United States | 3,690 | 41.9% |
| 2 | India | 972 | 11.0% |
| 3 | United Kingdom | 806 | 9.1% |
| 4 | Canada | 445 | 5.0% |
| 5 | France | 393 | 4.5% |
| 6 | Japan | 310 | 3.5% |
| 7 | Spain | 231 | 2.6% |
| 8 | South Korea | 225 | 2.6% |
| 9 | Mexico | 214 | 2.4% |
| 10 | Australia | 192 | 2.2% |

**Key insight:** The USA dominates production. India's strong #2 position reflects Netflix's aggressive expansion into the Indian market. South Korea's presence signals the K-Drama boom.

---

## 5. Content Ratings

| Rating | Count | Description |
|--------|-------|-------------|
| TV-MA | 3,207 | Mature audiences |
| TV-14 | 2,160 | Parental guidance (14+) |
| TV-PG | 863  | Parental guidance |
| R | 799 | Restricted |
| PG-13 | 490 | Parents cautioned |
| TV-Y | 307 | All children |

**Key insight:** Over 60% of content is rated TV-MA or TV-14, confirming Netflix's adult-centric content strategy. Family content (TV-Y, TV-Y7, G, PG) makes up under 15%.

---

## 6. Movie Duration

- **Minimum:** 3 minutes
- **Median:** ~98 minutes
- **Maximum:** 312 minutes
- **Average:** ~99 minutes

Most movies fall in the **80–120 minute** range, aligning with standard theatrical runtime conventions.

---

## 7. Seasonal Patterns

- **July** sees the highest average content additions
- **February** tends to be the slowest month
- Q3 (July–September) is consistently the peak quarter for additions

---

## 8. Key Recommendations for Netflix

1. **Invest more in TV Shows** — TV-14 and family categories are underserved vs. demand
2. **Expand regional content** — South Korea and India show strong ROI for local productions
3. **Diversify ratings** — Family content (G/PG) has growth potential
4. **Horror and Thriller gap** — These high-engagement genres are underrepresented vs. Dramas

---

## Methodology

- Data source: Kaggle Netflix Movies and TV Shows dataset
- Cleaning: nulls imputed, dates parsed, duplicates removed
- Analysis: Python (Pandas), SQL (SQLite), Matplotlib visualizations
- Bias note: Dataset may not reflect Netflix's full internal catalog; international availability varies

---

*Report generated from `notebooks/netflix_eda.ipynb`*
