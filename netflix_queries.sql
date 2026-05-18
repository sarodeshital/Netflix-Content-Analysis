-- ============================================================
-- Netflix Content Analysis — SQL Queries
-- Database : SQLite (also compatible with PostgreSQL/MySQL)
-- Dataset  : netflix_titles.csv (Kaggle)
-- ============================================================


-- ─────────────────────────────────────────────────────────────
-- 1. BASIC OVERVIEW
-- ─────────────────────────────────────────────────────────────

-- Total number of titles
SELECT COUNT(*) AS total_titles
FROM netflix;

-- Count by content type
SELECT
    type,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix), 1) AS percentage
FROM netflix
GROUP BY type
ORDER BY total DESC;

-- Dataset date range
SELECT
    MIN(release_year) AS earliest_release,
    MAX(release_year) AS latest_release,
    MIN(date_added)   AS first_added,
    MAX(date_added)   AS last_added
FROM netflix;


-- ─────────────────────────────────────────────────────────────
-- 2. CONTENT TRENDS OVER TIME
-- ─────────────────────────────────────────────────────────────

-- Titles added per year (all types)
SELECT
    year_added,
    COUNT(*) AS titles_added
FROM netflix
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;

-- Titles added per year, split by type
SELECT
    year_added,
    SUM(CASE WHEN type = 'Movie'   THEN 1 ELSE 0 END) AS movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
    COUNT(*) AS total
FROM netflix
WHERE year_added BETWEEN 2015 AND 2021
GROUP BY year_added
ORDER BY year_added;

-- Year-over-year growth rate
WITH yearly AS (
    SELECT year_added, COUNT(*) AS cnt
    FROM netflix
    WHERE year_added BETWEEN 2015 AND 2021
    GROUP BY year_added
)
SELECT
    year_added,
    cnt,
    LAG(cnt) OVER (ORDER BY year_added) AS prev_year,
    ROUND((cnt - LAG(cnt) OVER (ORDER BY year_added)) * 100.0
          / LAG(cnt) OVER (ORDER BY year_added), 1) AS yoy_growth_pct
FROM yearly;

-- Average titles added per month
SELECT
    month_added,
    ROUND(AVG(monthly_count), 0) AS avg_titles_per_month
FROM (
    SELECT
        month_added,
        year_added,
        COUNT(*) AS monthly_count
    FROM netflix
    WHERE month_added IS NOT NULL
    GROUP BY month_added, year_added
) sub
GROUP BY month_added
ORDER BY avg_titles_per_month DESC;


-- ─────────────────────────────────────────────────────────────
-- 3. GENRE ANALYSIS
-- ─────────────────────────────────────────────────────────────

-- NOTE: genres are stored comma-separated in 'listed_in'
-- Use application-side parsing (Python) for full genre explosion.

-- Titles per broad genre (SQLite LIKE approach)
SELECT 'Dramas'            AS genre, COUNT(*) AS count FROM netflix WHERE listed_in LIKE '%Dramas%'
UNION ALL
SELECT 'Comedies',                   COUNT(*) FROM netflix WHERE listed_in LIKE '%Comedies%'
UNION ALL
SELECT 'Documentaries',              COUNT(*) FROM netflix WHERE listed_in LIKE '%Documentaries%'
UNION ALL
SELECT 'Action & Adventure',         COUNT(*) FROM netflix WHERE listed_in LIKE '%Action & Adventure%'
UNION ALL
SELECT 'Thrillers',                  COUNT(*) FROM netflix WHERE listed_in LIKE '%Thrillers%'
UNION ALL
SELECT 'Children & Family Movies',   COUNT(*) FROM netflix WHERE listed_in LIKE '%Children & Family%'
UNION ALL
SELECT 'Romantic Movies',            COUNT(*) FROM netflix WHERE listed_in LIKE '%Romantic Movies%'
UNION ALL
SELECT 'Horror Movies',              COUNT(*) FROM netflix WHERE listed_in LIKE '%Horror Movies%'
UNION ALL
SELECT 'Crime TV Shows',             COUNT(*) FROM netflix WHERE listed_in LIKE '%Crime TV%'
UNION ALL
SELECT 'Stand-Up Comedy',            COUNT(*) FROM netflix WHERE listed_in LIKE '%Stand-Up%'
ORDER BY count DESC;

-- Genre preference: Movies vs TV Shows
SELECT
    type,
    SUM(CASE WHEN listed_in LIKE '%Dramas%'    THEN 1 ELSE 0 END) AS dramas,
    SUM(CASE WHEN listed_in LIKE '%Comedies%'  THEN 1 ELSE 0 END) AS comedies,
    SUM(CASE WHEN listed_in LIKE '%Documentaries%' THEN 1 ELSE 0 END) AS documentaries,
    SUM(CASE WHEN listed_in LIKE '%Thrillers%' THEN 1 ELSE 0 END) AS thrillers
FROM netflix
GROUP BY type;


-- ─────────────────────────────────────────────────────────────
-- 4. COUNTRY DISTRIBUTION
-- ─────────────────────────────────────────────────────────────

-- Top 10 countries by total titles (primary country only)
SELECT
    country,
    COUNT(*) AS titles,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix WHERE country != 'Unknown'), 1) AS pct
FROM netflix
WHERE country != 'Unknown'
GROUP BY country
ORDER BY titles DESC
LIMIT 10;

-- Countries producing both Movies and TV Shows
SELECT
    country,
    SUM(CASE WHEN type = 'Movie'   THEN 1 ELSE 0 END) AS movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows,
    COUNT(*) AS total
FROM netflix
WHERE country != 'Unknown'
GROUP BY country
HAVING movies > 0 AND tv_shows > 0
ORDER BY total DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- 5. RATINGS ANALYSIS
-- ─────────────────────────────────────────────────────────────

-- Rating distribution
SELECT
    rating,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix), 1) AS pct
FROM netflix
WHERE rating NOT IN ('Unknown', 'Not Rated', 'UR')
GROUP BY rating
ORDER BY count DESC;

-- Rating by content type
SELECT
    rating,
    SUM(CASE WHEN type = 'Movie'   THEN 1 ELSE 0 END) AS movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_shows
FROM netflix
WHERE rating NOT IN ('Unknown', 'Not Rated')
GROUP BY rating
ORDER BY (movies + tv_shows) DESC;


-- ─────────────────────────────────────────────────────────────
-- 6. DIRECTORS & CAST
-- ─────────────────────────────────────────────────────────────

-- Top 10 directors
SELECT
    director,
    COUNT(*) AS titles_directed,
    GROUP_CONCAT(DISTINCT type) AS content_types
FROM netflix
WHERE director != 'Unknown'
GROUP BY director
ORDER BY titles_directed DESC
LIMIT 10;

-- Most prolific directors per country
SELECT
    country,
    director,
    COUNT(*) AS titles
FROM netflix
WHERE director != 'Unknown' AND country != 'Unknown'
GROUP BY country, director
ORDER BY country, titles DESC;


-- ─────────────────────────────────────────────────────────────
-- 7. DURATION ANALYSIS
-- ─────────────────────────────────────────────────────────────

-- Movie duration stats
SELECT
    MIN(duration_value)                       AS min_minutes,
    MAX(duration_value)                       AS max_minutes,
    ROUND(AVG(duration_value), 1)             AS avg_minutes,
    ROUND(AVG(duration_value) / 60.0, 2)     AS avg_hours
FROM netflix
WHERE type = 'Movie' AND duration_value IS NOT NULL;

-- TV Show season distribution
SELECT
    duration_value AS seasons,
    COUNT(*) AS shows
FROM netflix
WHERE type = 'TV Show' AND duration_value IS NOT NULL
GROUP BY duration_value
ORDER BY duration_value;

-- Long movies (> 2 hours)
SELECT title, country, release_year, duration
FROM netflix
WHERE type = 'Movie' AND duration_value > 120
ORDER BY duration_value DESC
LIMIT 15;


-- ─────────────────────────────────────────────────────────────
-- 8. ADVANCED QUERIES
-- ─────────────────────────────────────────────────────────────

-- Most recent additions per country
SELECT
    country,
    title,
    type,
    date_added
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY country ORDER BY date_added DESC) AS rn
    FROM netflix
    WHERE country != 'Unknown'
) t
WHERE rn = 1
ORDER BY date_added DESC
LIMIT 10;

-- Titles added in the last 2 years of the dataset
SELECT
    title,
    type,
    country,
    date_added,
    listed_in
FROM netflix
WHERE date_added >= DATE((SELECT MAX(date_added) FROM netflix), '-2 years')
ORDER BY date_added DESC
LIMIT 20;

-- Content diversity score per country (unique genres / total titles)
SELECT
    country,
    COUNT(*) AS total_titles,
    COUNT(DISTINCT listed_in) AS unique_genre_combos,
    ROUND(COUNT(DISTINCT listed_in) * 1.0 / COUNT(*), 3) AS diversity_score
FROM netflix
WHERE country != 'Unknown'
GROUP BY country
HAVING total_titles >= 20
ORDER BY diversity_score DESC
LIMIT 10;
