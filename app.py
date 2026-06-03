import streamlit as st
from filters import load_data, apply_filters
import charts

# ── CONFIGURATION ──
st.set_page_config(page_title="Sea Level Dashboard",
                   page_icon="🌊",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── CSS VARIABLES ── */
:root {
    --rose-100: #fff1f2;
    --rose-200: #ffe4e6;
    --rose-300: #fda4af;
    --rose-400: #fb7185;
    --rose-500: #f43f5e;
    --rose-600: #e11d48;
    --blush-soft: #fce7f3;
    --blush-mid: #fbcfe8;
    --mauve: #c084fc;
    --text-dark: #1a0a0e;
    --text-light: #f9f0f2;
}

/* ── TYPOGRAPHY BASELINE ── */
* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .hero-title { font-family: 'Cormorant Garamond', serif; }

/* ── LAYOUT ── */
.block-container {
    padding-top: 1.5rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(244,63,94,0.15);
    background: var(--secondary-background-color) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1rem; }
[data-testid="stSidebar"] label {
    color: var(--rose-500) !important;
    font-size: 0.67rem !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 600;
}
[data-testid="stSidebar"] input {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(244,63,94,0.25) !important;
    color: var(--text-color) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: var(--text-color) !important;
    opacity: 0.4 !important;
}

/* Slider accent */
[data-testid="stSlider"] [role="slider"] {
    background: var(--rose-500) !important;
    border-color: var(--rose-400) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    background: linear-gradient(90deg, var(--rose-400), var(--rose-300)) !important;
}

.sidebar-title {
    color: var(--text-color) !important;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(244,63,94,0.2);
    margin-bottom: 1.2rem;
}
.stButton > button {
    background: linear-gradient(135deg, var(--rose-500), var(--rose-400)) !important;
    border: none !important;
    color: white !important;
    width: 100%;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.55rem !important;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(244,63,94,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(244,63,94,0.35) !important;
}

/* ── HERO ── */
.hero {
    background: var(--secondary-background-color);
    border: 1px solid rgba(244,63,94,0.18);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(0.25,0.8,0.25,1), box-shadow 0.35s ease;
}
.hero:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(244,63,94,0.1);
    border-color: rgba(244,63,94,0.32);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(244,63,94,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--rose-400), var(--rose-300), transparent);
}
.hero-eyebrow {
    font-size: 0.67rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--rose-400) !important; margin-bottom: 0.9rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem; font-weight: 600; color: var(--text-color) !important;
    line-height: 1.05; letter-spacing: -0.01em; margin-bottom: 0.9rem;
}
.hero-title em { font-style: italic; color: var(--rose-500) !important; }
.hero-desc {
    font-size: 0.87rem; color: var(--text-color) !important;
    opacity: 0.65; max-width: 520px; line-height: 1.7;
}

/* ── METRIC CARDS ── */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.metric-item {
    background: var(--secondary-background-color);
    border: 1px solid rgba(244,63,94,0.14);
    border-radius: 12px; padding: 1.3rem 1.5rem; position: relative; overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.metric-item:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 24px rgba(244,63,94,0.1);
    border-color: rgba(244,63,94,0.3);
    z-index: 10;
}
.metric-item::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    transition: height 0.3s ease;
}
.metric-item:hover::before { height: 4px; }
.metric-item.rose::before   { background: linear-gradient(90deg, #f43f5e, #fb7185); }
.metric-item.blush::before  { background: linear-gradient(90deg, #fb7185, #fda4af); }
.metric-item.mauve::before  { background: linear-gradient(90deg, #c084fc, #e879f9); }
.metric-item.warm::before   { background: linear-gradient(90deg, #fb923c, #f43f5e); }
.metric-label {
    font-size: 0.64rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.14em;
    color: var(--text-color) !important; opacity: 0.55; margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem; font-weight: 600; color: var(--text-color) !important; line-height: 1;
}
.metric-sub { font-size: 0.71rem; color: var(--text-color) !important; opacity: 0.45; margin-top: 0.3rem; }

/* ── CHART CARDS ── */
.chart-card {
    background: var(--secondary-background-color);
    border: 1px solid rgba(244,63,94,0.14);
    border-radius: 14px; padding: 1.6rem; margin-bottom: 1.2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.chart-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(244,63,94,0.09);
    border-color: rgba(244,63,94,0.28);
}

/* ── FIX: Charts blend naturally, no white box ── */
[data-testid="stImage"] {
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
}
/* matplotlib figures rendered via st.pyplot get a figure wrapper */
[data-testid="stImage"] img {
    border-radius: 8px;
    width: 100%;
}
.chart-card-header {
    display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 1rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(244,63,94,0.1);
}
.chart-num {
    background: linear-gradient(135deg, var(--rose-500), var(--rose-400));
    color: white !important; font-size: 0.58rem; font-weight: 700;
    min-width: 22px; height: 22px; border-radius: 6px;
    display: inline-flex; align-items: center; justify-content: center; margin-top: 2px;
}
.chart-info-title { font-size: 0.95rem; font-weight: 600; color: var(--text-color) !important; margin: 0; }
.chart-info-desc  { font-size: 0.75rem; color: var(--text-color) !important; opacity: 0.55; margin: 0.15rem 0 0 0; }

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.61rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.22em;
    color: var(--rose-400) !important; margin: 1.8rem 0 1rem 0;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(244,63,94,0.18); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(244,63,94,0.18) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-color) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.1rem !important;
    margin: 0 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(244,63,94,0.07) !important;
    transform: translateY(-1px);
}
.stTabs [aria-selected="true"] {
    background: rgba(244,63,94,0.12) !important;
    color: var(--rose-500) !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 10px rgba(244,63,94,0.18);
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(244,63,94,0.14) !important;
    border-radius: 10px !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌸 Filter Data</div>', unsafe_allow_html=True)
    year_range = st.slider("Year Range",
                           float(df['year'].min()), float(df['year'].max()),
                           (float(df['year'].min()), float(df['year'].max())))
    era = st.selectbox("Era", ['All', '1990s', '2000s', '2010s', '2020s'])
    altimeter = st.selectbox("Altimeter Type",
                             ['All', 'Dual Frequency', 'Single Frequency'])
    gmsl_min = float(df['gmsl_gia'].min())
    gmsl_max = float(df['gmsl_gia'].max())
    gmsl_range = st.slider("Sea Level Range (mm)",
                           gmsl_min, gmsl_max, (gmsl_min, gmsl_max))
    search = st.text_input("Search by Year", placeholder="e.g. 2010")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset Filters"):
        st.rerun()

filtered_df = apply_filters(df, year_range, era, altimeter, gmsl_range, search)

# ── HERO ──
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">NASA Satellite Altimeter Data</div>
    <div class="hero-title">Global Mean<br><em>Sea Level Rise</em></div>
    <div class="hero-desc">
        Tracking ocean level changes using TOPEX/Poseidon, Jason-1, Jason-2,
        Jason-3 and Sentinel-6 satellite measurements from 1993 to 2025.
    </div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-item rose">
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{len(filtered_df):,}</div>
        <div class="metric-sub">measurements filtered</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-item blush">
        <div class="metric-label">Peak Sea Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].max():.1f}<span style="font-size:1rem">mm</span></div>
        <div class="metric-sub">highest recorded</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-item mauve">
        <div class="metric-label">Average Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].mean():.1f}<span style="font-size:1rem">mm</span></div>
        <div class="metric-sub">mean variation</div>
    </div>""", unsafe_allow_html=True)
with m4:
    total_rise = filtered_df['gmsl_gia'].max() - filtered_df['gmsl_gia'].min()
    st.markdown(f"""
    <div class="metric-item warm">
        <div class="metric-label">Total Rise</div>
        <div class="metric-value">{total_rise:.1f}<span style="font-size:1rem">mm</span></div>
        <div class="metric-sub">over selected period</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Distribution", "Trends", "Relationships", "Data Table", "Bonus Charts"
])

# ── TAB 1 ──
with tab1:
    st.markdown('<div class="section-label">Proportional and Frequency Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">1</span>
        <div><p class="chart-info-title">Altimeter Type Distribution</p>
        <p class="chart-info-desc">Proportional split between dual and single frequency altimeter types</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.pie_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">2</span>
        <div><p class="chart-info-title">Sea Level Variation Distribution</p>
        <p class="chart-info-desc">Frequency histogram of GMSL values across all measurements</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.histogram(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">9</span>
        <div><p class="chart-info-title">Measurements by Altimeter Type</p>
        <p class="chart-info-desc">Count of total readings taken by each altimeter instrument</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.count_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 2 ──
with tab2:
    st.markdown('<div class="section-label">Trends Over Time and Categories</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">3</span>
        <div><p class="chart-info-title">Sea Level Rise Over Time</p>
        <p class="chart-info-desc">Raw and smoothed GMSL from 1993 to 2025 showing clear upward trend</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.line_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">4</span>
        <div><p class="chart-info-title">Average Sea Level by Decade</p>
        <p class="chart-info-desc">Bar comparison of mean sea level values across each decade</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.bar_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">8</span>
        <div><p class="chart-info-title">Cumulative Sea Level Rise</p>
        <p class="chart-info-desc">Area chart showing the total accumulated rise over the entire period</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.area_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 3 ──
with tab3:
    st.markdown('<div class="section-label">Statistical Relationships and Distributions</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">5</span>
        <div><p class="chart-info-title">GIA vs Non-GIA Measurements</p>
        <p class="chart-info-desc">Scatter relationship between corrected and uncorrected sea level readings</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.scatter_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">6</span>
        <div><p class="chart-info-title">Sea Level Distribution by Era</p>
        <p class="chart-info-desc">Box plot showing spread, median and outliers per era</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.box_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">7</span>
        <div><p class="chart-info-title">Feature Correlation Heatmap</p>
        <p class="chart-info-desc">Correlation matrix between all sea level measurement variables</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.heatmap(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">10</span>
        <div><p class="chart-info-title">Sea Level Density by Era</p>
        <p class="chart-info-desc">Violin plot showing probability density of sea level per era</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.violin_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4 ──
with tab4:
    st.markdown('<div class="section-label">Raw Data and Statistics</div>', unsafe_allow_html=True)
    display_cols = ['year', 'era', 'gmsl_gia', 'smooth_gia',
                    'std_gia', 'altimeter_label', 'num_observations']
    st.dataframe(filtered_df[display_cols].round(2),
                 use_container_width=True, height=450)
    
    st.markdown('<div class="section-label">Summary Statistics</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df[['gmsl_gia', 'smooth_gia', 'std_gia']].describe().round(2),
        use_container_width=True)

# ── TAB 5 ──
with tab5:
    st.markdown('<div class="section-label">Bonus Visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">+</span>
        <div><p class="chart-info-title">Pair Plot — Sea Level Features</p>
        <p class="chart-info-desc">Relationships between all sea level measurement variables combined</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.pair_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">+</span>
        <div><p class="chart-info-title">Bubble Chart — Sea Level by Decade</p>
        <p class="chart-info-desc">Bubble size = total observations. Color intensity = sea level rise.</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.bubble_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">+</span>
        <div><p class="chart-info-title">Funnel Chart — Measurements by Era</p>
        <p class="chart-info-desc">Distribution of total satellite measurements across time eras</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.funnel_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)