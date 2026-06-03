import streamlit as st
from filters import load_data, apply_filters
import charts

# ── CONFIGURATION ──
st.set_page_config(page_title="Sea Level Dashboard", 
                   page_icon="🌊", 
                   layout="wide",
                   initial_sidebar_state="expanded")

# Injecting dynamic CSS using Streamlit's native variables to support BOTH Light and Dark modes
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* Typography baseline */
* { font-family: 'Space Grotesk', sans-serif; }

/* Remove top padding block */
.block-container { 
    padding-top: 1.5rem !important; 
    max-width: 100% !important;
}
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }

/* Let Streamlit handle menu colors dynamically */
[data-testid="stDecoration"] { display: none !important; }

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.2);
}
[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1rem; }
[data-testid="stSidebar"] label {
    color: #00ccff !important;
    font-size: 0.68rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
}

/* Input controls adapting to light/dark mode */
[data-testid="stSidebar"] input {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(128,128,128,0.3) !important;
    color: var(--text-color) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: var(--text-color) !important;
    opacity: 0.4 !important;
}

.sidebar-title {
    color: var(--text-color) !important;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(128,128,128,0.2);
    margin-bottom: 1.2rem;
}

.stButton > button {
    background: linear-gradient(135deg, #0066ff, #00ccff) !important;
    border: none !important;
    color: white !important; /* Button text stays white on the blue gradient */
    width: 100%;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.5rem !important;
    margin-top: 0.5rem;
}

/* HERO SECTION */
.hero {
    background: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00ccff, #0066ff, transparent);
}
.hero-eyebrow {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase;
    color: #00ccff !important; margin-bottom: 0.8rem;
}
.hero-title {
    font-size: 3rem; font-weight: 700; color: var(--text-color) !important;
    line-height: 1.05; letter-spacing: -0.02em; margin-bottom: 0.8rem;
}
.hero-title em { font-style: normal; color: #00ccff !important; }
.hero-desc {
    font-size: 0.88rem; color: var(--text-color) !important; opacity: 0.7; max-width: 500px; line-height: 1.6;
}

/* METRIC CARDS */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.metric-item {
    background: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 10px; padding: 1.2rem 1.5rem; position: relative; overflow: hidden;
}
.metric-item::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.metric-item.blue::before { background: linear-gradient(90deg, #0066ff, #00ccff); }
.metric-item.teal::before { background: linear-gradient(90deg, #00ccff, #00ffcc); }
.metric-item.purple::before { background: linear-gradient(90deg, #7c3aed, #a855f7); }
.metric-item.orange::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }
.metric-label {
    font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em;
    color: var(--text-color) !important; opacity: 0.6; margin-bottom: 0.4rem;
}
.metric-value { font-size: 1.8rem; font-weight: 700; color: var(--text-color) !important; line-height: 1; }
.metric-sub { font-size: 0.72rem; color: var(--text-color) !important; opacity: 0.5; margin-top: 0.3rem; }

/* CHARTS */
.chart-card {
    background: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem;
}
.chart-card-header {
    display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 1rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(128,128,128,0.1);
}
.chart-num {
    background: linear-gradient(135deg, #0066ff, #00ccff); color: white !important; font-size: 0.6rem;
    font-weight: 700; min-width: 22px; height: 22px; border-radius: 6px; display: inline-flex;
    align-items: center; justify-content: center; margin-top: 2px;
}
.chart-info-title { font-size: 0.95rem; font-weight: 600; color: var(--text-color) !important; margin: 0; }
.chart-info-desc { font-size: 0.75rem; color: var(--text-color) !important; opacity: 0.6; margin: 0.15rem 0 0 0; }

.section-label {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em;
    color: #00ccff !important; margin: 1.8rem 0 1rem 0; display: flex; align-items: center; gap: 0.6rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(128,128,128,0.2); }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(128,128,128,0.2) !important;
    border-radius: 10px !important; padding: 3px !important; gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 7px !important;
    color: var(--text-color) !important; font-size: 0.8rem !important; font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,200,255,0.12) !important; color: #00ccff !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌊 Filter Data</div>', unsafe_allow_html=True)

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
    <div class="metric-item blue">
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{len(filtered_df):,}</div>
        <div class="metric-sub">measurements filtered</div>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-item teal">
        <div class="metric-label">Peak Sea Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].max():.1f}<span style="font-size:1rem">mm</span></div>
        <div class="metric-sub">highest recorded</div>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-item purple">
        <div class="metric-label">Average Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].mean():.1f}<span style="font-size:1rem">mm</span></div>
        <div class="metric-sub">mean variation</div>
    </div>""", unsafe_allow_html=True)

with m4:
    total_rise = filtered_df['gmsl_gia'].max() - filtered_df['gmsl_gia'].min()
    st.markdown(f"""
    <div class="metric-item orange">
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
    st.pyplot(charts.pie_chart(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">2</span>
        <div><p class="chart-info-title">Sea Level Variation Distribution</p>
        <p class="chart-info-desc">Frequency histogram of GMSL values across all measurements</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.histogram(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">9</span>
        <div><p class="chart-info-title">Measurements by Altimeter Type</p>
        <p class="chart-info-desc">Count of total readings taken by each altimeter instrument</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.count_plot(filtered_df), theme="streamlit")
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
    st.pyplot(charts.line_chart(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">4</span>
        <div><p class="chart-info-title">Average Sea Level by Decade</p>
        <p class="chart-info-desc">Bar comparison of mean sea level values across each decade</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.bar_chart(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">8</span>
        <div><p class="chart-info-title">Cumulative Sea Level Rise</p>
        <p class="chart-info-desc">Area chart showing the total accumulated rise over the entire period</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.area_chart(filtered_df), theme="streamlit")
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
    st.pyplot(charts.scatter_plot(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">6</span>
        <div><p class="chart-info-title">Sea Level Distribution by Era</p>
        <p class="chart-info-desc">Box plot showing spread, median and outliers per era</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.box_plot(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">7</span>
        <div><p class="chart-info-title">Feature Correlation Heatmap</p>
        <p class="chart-info-desc">Correlation matrix between all sea level measurement variables</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.heatmap(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">10</span>
        <div><p class="chart-info-title">Sea Level Density by Era</p>
        <p class="chart-info-desc">Violin plot showing probability density of sea level per era</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.violin_plot(filtered_df), theme="streamlit")
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
        <div><p class="chart-info-title">Pair Plot - Sea Level Features</p>
        <p class="chart-info-desc">Relationships between all sea level measurement variables combined</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.pair_plot(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">+</span>
        <div><p class="chart-info-title">Bubble Chart - Sea Level by Decade</p>
        <p class="chart-info-desc">Bubble size = total observations. Color intensity = sea level rise.</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.bubble_chart(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""<div class="chart-card-header">
        <span class="chart-num">+</span>
        <div><p class="chart-info-title">Funnel Chart - Measurements by Era</p>
        <p class="chart-info-desc">Distribution of total satellite measurements across time eras</p></div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(charts.funnel_chart(filtered_df), theme="streamlit")
    st.markdown('</div>', unsafe_allow_html=True)