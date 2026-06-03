# Global Mean Sea Level Dashboard

## Course: Exploratory Data Analysis
## Instructor: Ali Hassan Sherazi

---

## Project Overview
An interactive dashboard analyzing Global Mean Sea Level (GMSL)
data from NASA covering 1993 to 2025. The data tracks sea level
rise using satellite altimeter measurements.

---

## Dataset
- GMSL_TPJAOS_5.2.txt — NASA Global Mean Sea Level measurements
- Source: NASA Goddard Space Flight Center

---

## How to Install Dependencies
Open terminal and run:
pip install pandas numpy matplotlib seaborn streamlit

---

## How to Run the Dashboard
1. Open Command Prompt
2. Navigate to project folder
3. Run: python -m streamlit run app.py
4. Dashboard opens at localhost:8501

---

## Key Insights
- Sea levels have risen significantly from 1993 to 2025
- Average rise of over 100mm observed over 30 years
- Dual frequency altimeters dominate the measurements
- Clear upward trend visible especially after 2010
- Seasonal variations visible in raw data but removed in smoothed version

---

## Charts Included
1. Pie Chart - Altimeter Type Distribution
2. Histogram - Sea Level Variation Distribution
3. Line Chart - Sea Level Rise Over Time
4. Bar Chart - Average Sea Level by Decade
5. Scatter Plot - GIA vs Non-GIA Measurements
6. Box Plot - Sea Level Distribution by Era
7. Heatmap - Feature Correlation Matrix
8. Area Chart - Cumulative Sea Level Rise
9. Count Plot - Measurements by Altimeter Type
10. Violin Plot - Sea Level Distribution by Era
11. Pair Plot (Bonus)
12. Bubble Chart (Bonus)
13. Funnel Chart (Bonus)