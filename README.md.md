# 🎬 Netflix Content Analysis

> **Exploratory Data Analysis of Netflix Movies and TV Shows using Python, Data Visualization, and SQL**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4C72B0)](https://seaborn.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-SQL-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## 📌 Project Overview

This project performs an exploratory analysis of the **Netflix Movies and TV Shows** dataset.

The analysis focuses on understanding Netflix's content library through data cleaning, descriptive statistics, visualization, and SQL queries. It examines content type, content trends over time, genres, countries, ratings, directors, and movie duration.

**Author:** Shital Sarode  
**Dataset:** Netflix Movies and TV Shows  
**Dataset source:** [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

## 🎯 Objectives

The main objectives of this project are to:

- Load and inspect the Netflix dataset.
- Identify missing values and clean the data.
- Compare Movies and TV Shows.
- Analyze content additions over time.
- Identify the most common genres.
- Examine content-producing countries.
- Analyze content ratings.
- Explore director-level information.
- Analyze movie duration.
- Perform SQL-based analysis using SQLite.
- Present findings through clear visualizations.

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Data analysis and programming |
| **Pandas** | Data loading, cleaning, transformation, and analysis |
| **NumPy** | Numerical operations |
| **Matplotlib** | Data visualization |
| **Seaborn** | Statistical/data visualization |
| **SQLite** | SQL-based analysis |
| **Jupyter Notebook** | Interactive analysis and presentation |

---

## 📂 Project Structure

```text
Netflix-Content-Analysis/
│
├── data/
│   └── netflix_titles.csv
│
├── notebooks/
│   └── Netflix_Content_Analysis.ipynb
│
├── visualizations/
│   ├── 01_content_type_split.png
│   ├── 02_yearly_additions.png
│   ├── 03_top_genres.png
│   ├── 04_top_countries.png
│   ├── 05_rating_distribution.png
│   ├── 07_top_directors.png
│   └── 08_movie_duration.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔎 Analysis Workflow

### 1. Setup & Data Loading

The project loads the Netflix dataset using Pandas and inspects its structure, dimensions, and available fields.

### 2. Data Cleaning

The analysis handles missing values in fields such as:

- Director
- Cast
- Country
- Rating

The `date_added` field is parsed into a datetime format, and additional fields such as `year_added`, `month_added`, and `month_num` are created.

Movie duration is also extracted into a numerical field for analysis.

### 3. Summary Statistics

The project calculates summary information including:

- Total number of titles
- Number of Movies
- Number of TV Shows
- Number of countries
- Release-year range
- Average movie duration
- Most common rating
- Most common genre

### 4. Movies vs TV Shows

A visualization compares the distribution of Movies and TV Shows in the Netflix library.

### 5. Content Trends Over Time

The project analyzes content additions from **2015 to 2021**, comparing Movies and TV Shows by year.

### 6. Genre Analysis

The dataset's genre information is split and analyzed to identify the **Top 10 genres**.

### 7. Country Distribution

The project analyzes country information and identifies the **Top 10 content-producing countries**.

### 8. Rating Analysis

The project examines the distribution of content ratings, including ratings such as:

- G
- PG
- PG-13
- R
- TV-Y
- TV-Y7
- TV-G
- TV-PG
- TV-14
- TV-MA
- NR

### 9. Director Insights

Director information is analyzed to identify the **Top 10 directors** by number of titles.

### 10. Duration Analysis

Movie durations are converted to numerical values and analyzed using a histogram and descriptive statistics.

### 11. SQL Analysis

The project uses an in-memory SQLite database to perform SQL analysis, including:

- Top countries
- Year-over-year content additions
- Top directors and their content types

### 12. Key Findings

The notebook reports the following findings from the analyzed dataset:

1. **Movies dominate** — approximately 69.6% of the library.
2. **Peak growth in 2019** — content additions reached an all-time high.
3. **Dramas are the most popular genre** across Movies and TV Shows.
4. **USA is the top producer** with approximately 42% of all titles.
5. **TV-MA is the most common rating**.
6. **India is #2** in content production in the analysis.
7. A typical movie is approximately **90–100 minutes** long based on the reported median.
8. **July is the peak month** for new content additions.

> These findings are specific to the dataset and analysis performed in this project and should not be interpreted as current Netflix catalog statistics.

---

## 📊 Visualizations

The project generates the following visualizations:

| Visualization | Description |
|---|---|
| `01_content_type_split.png` | Movies vs TV Shows |
| `02_yearly_additions.png` | Content added by year |
| `03_top_genres.png` | Top 10 genres |
| `04_top_countries.png` | Top 10 content-producing countries |
| `05_rating_distribution.png` | Content rating distribution |
| `07_top_directors.png` | Top 10 directors |
| `08_movie_duration.png` | Movie duration distribution |

---

## 🚀 Getting Started

### Prerequisites

Install **Python 3.10 or newer**.

Check your Python version:

```bash
python --version
```

### 1. Clone the repository

```bash
git clone https://github.com/sarodeshital/Netflix-Content-Analysis.git
cd Netflix-Content-Analysis
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/Netflix_Content_Analysis.ipynb
```

### 5. Verify the dataset path

The notebook expects the dataset at:

```text
data/netflix_titles.csv
```

---

## 💻 Run with JupyterLab

If you prefer JupyterLab:

```bash
pip install jupyterlab
jupyter lab
```

Then open the notebook from the `notebooks/` folder.

---

## 📈 Example Analysis

The project includes analysis such as:

```python
counts = df['type'].value_counts()
print(counts)
```

and SQL queries such as:

```sql
SELECT country, COUNT(*) AS titles
FROM netflix
WHERE country != 'Unknown'
GROUP BY country
ORDER BY titles DESC
LIMIT 10;
```

---

## 🧹 Data Cleaning Approach

The project replaces missing categorical information with explicit values such as:

```text
Unknown
Not Rated
```

Rows without `date_added` are removed because the project uses the date for time-based analysis.

The `date_added` column is converted to datetime and used to derive:

```text
year_added
month_added
month_num
```

Movie duration is converted into a numerical field for statistical analysis.

---

## 📚 Dataset

The project uses the **Netflix Movies and TV Shows** dataset available through Kaggle:

**Kaggle:**  
https://www.kaggle.com/datasets/shivamb/netflix-shows

Please refer to the original dataset page for dataset-specific licensing and attribution information.

---

## ⚠️ Limitations

- The analysis is based on the provided Kaggle dataset rather than Netflix's live catalog.
- Country and genre fields can contain multiple values per title.
- Missing values are handled using project-specific assumptions such as `Unknown` and `Not Rated`.
- The reported findings describe the analyzed dataset and its available date range.
- Historical dataset patterns should not automatically be interpreted as current Netflix business statistics.

---

## 🔮 Possible Future Improvements

This project can be extended with:

- Interactive dashboards using **Power BI** or **Tableau**
- Interactive visualizations using **Plotly**
- More advanced SQL analysis
- Time-series analysis
- Genre trends by year
- Country-level trend analysis
- Director and actor network analysis
- Recommendation-system experimentation
- Statistical hypothesis testing
- Machine learning models for classification or prediction

---

## 👨‍💻 Author

**Shital Sarode**

This project was created as a data analytics portfolio project demonstrating skills in:

- Data Cleaning
- Exploratory Data Analysis
- Data Visualization
- Python
- Pandas
- SQL
- SQLite
- Jupyter Notebook

---

## ⭐ If You Find This Project Useful

Feel free to explore the notebook, review the visualizations, and use the project structure as a reference for your own data-analysis projects.

