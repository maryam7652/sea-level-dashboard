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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap');

/* Typography baseline */
* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .hero-title, .sidebar-title, .metric-value { 
    font-family: 'Cormorant Garamond', serif; 
}

/* Remove top padding */
.block-container { 
    padding-top: 1.5rem !important; 
    max-width: 100% !important;
}
header[data-testid="stHeader"], [data-testid="stDecoration"] { 
    display: none !important; 
}

/* =========================================
   DYNAMIC PINK BACKGROUND THEME
   ========================================= */

/* LIGHT MODE (BABY PINK) - DEFAULT */
[data-testid="stAppViewContainer"] {
    background-color: #ffe4e6 !important; 
}
[data-testid="stSidebar"] {
    background-color: #fce7f3 !important; 
    border-right: 1px solid rgba(244, 63, 94, 0.2) !important;
}
.chart-card, .metric-item, .hero {
    background-color: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(244, 63, 94, 0.25) !important;
    box-shadow: 0 8px 20px rgba(244, 63, 94, 0.08);
}
.hero-title, .metric-value, .chart-info-title, .sidebar-title {
    color: #4c0519 !important; 
}
p, span, label, .hero-desc, .metric-sub, .chart-info-desc {
    color: #881337 !important; 
}
.chart-card-header {
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.08), transparent);
}

/* DARK MODE (DARK PINK / MAROON) - TRIGGERED BY SYSTEM SETTING */
@media (prefers-color-scheme: dark) {
    [data-testid="stAppViewContainer"] {
        background-color: #380b1b !important; 
    }
    [data-testid="stSidebar"] {
        background-color: #2d0513 !important; 
        border-right: 1px solid rgba(244, 63, 94, 0.3) !important;
    }
    .chart-card, .metric-item, .hero {
        background-color: rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(244, 63, 94, 0.35) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    .hero-title, .metric-value, .chart-info-title, .sidebar-title {
        color: #ffe4e6 !important; 
    }
    p, span, label, .hero-desc, .metric-sub, .chart-info-desc {
        color: #fda4af !important; 
    }
    .chart-card-header {
        background: linear-gradient(90deg, rgba(244, 63, 94, 0.2), transparent) !important;
    }
}

/* =========================================
   UI ELEMENTS & EFFECTS
   ========================================= */

/* Sidebar Inputs */
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
    border-radius: 8px !important;
}

/* Fix Multi-Select Tags */
.stMultiSelect [data-baseweb="tag"] {
    background-color: rgba(244, 63, 94, 0.15) !important;
    color: #f43f5e !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
    border-radius: 6px !important;
}
@media (prefers-color-scheme: dark) {
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(244, 63, 94, 0.3) !important;
        color: #ffe4e6 !important;
    }
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #f43f5e, #fb7185) !important;
    border: none !important;
    color: white !important;
    width: 100%;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(244, 63, 94, 0.4) !important;
}

/* Hero Section Base */
.hero {
    padding: 2.8rem 3rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
    transition: transform 0.35s ease;
}
.hero:hover { transform: translateY(-3px); }
.hero-eyebrow {
    font-size: 0.67rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase;
    color: #fb7185 !important; margin-bottom: 0.9rem;
}
.hero-title { font-size: 3.2rem; line-height: 1.05; margin-bottom: 0.9rem; }
.hero-title em { font-style: italic; color: #f43f5e !important; }

/* Metric Cards Layout */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.metric-item {
    border-radius: 12px; padding: 1.3rem 1.5rem; position: relative;
    transition: transform 0.3s ease;
}
.metric-item:hover { transform: translateY(-4px) scale(1.02); }
.metric-item::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.metric-item.rose::before   { background: linear-gradient(90deg, #f43f5e, #fb7185); }
.metric-item.blush::before  { background: linear-gradient(90deg, #fb7185, #fda4af); }
.metric-item.mauve::before  { background: linear-gradient(90deg, #d946ef, #f43f5e); }
.metric-item.warm::before   { background: linear-gradient(90deg, #be123c, #e11d48); }

.metric-label { font-size: 0.64rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; }
.metric-value { font-size: 2rem; }

/* ── EDITORIAL CHART HEADERS ── */
.chart-card { border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
.chart-card-header {
    display: flex; align-items: center; gap: 1.2rem; margin-bottom: 1.5rem; padding: 1rem 1.2rem;
    border-radius: 10px;
    border-left: 4px solid #f43f5e;
}
.chart-card-header > div {
    display: flex; flex-direction: column; gap: 0.2rem;
}
.chart-num {
    background: linear-gradient(135deg, #e11d48, #fb7185); color: white !important; 
    font-size: 0.95rem; font-weight: 700; min-width: 36px; height: 36px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 10px rgba(225, 29, 72, 0.3); margin: 0; flex-shrink: 0;
}
.chart-info-title { 
    font-family: 'Cormorant Garamond', serif !important; 
    font-size: 1.45rem !important; font-weight: 700 !important; 
    margin: 0 !important; line-height: 1.1; 
}
.chart-info-desc { 
    font-size: 0.88rem !important; font-weight: 500; opacity: 0.85; margin: 0 !important; 
}

/* Tabs - Fixed Padding and Layout */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 8px !important;
    padding-bottom: 10px !important;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(244, 63, 94, 0.1) !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    border: 1px solid transparent !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(244, 63, 94, 0.25) !important;
    border: 1px solid rgba(244, 63, 94, 0.4) !important;
    color: #f43f5e !important;
}

/* Ensure Matplotlib background doesn't render a white box */
[data-testid="stImage"] { background: transparent !important; box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌸 Filter Data</div>', unsafe_allow_html=True)
    
    year_range = st.slider("Year Range", float(df['year'].min()), float(df['year'].max()), (float(df['year'].min()), float(df['year'].max())))
    
    era = st.multiselect("Era", 
                         ['1990s', '2000s', '2010s', '2020s'],
                         default=['1990s', '2000s', '2010s', '2020s'])
                         
    altimeter = st.selectbox("Altimeter Type", ['All', 'Dual Frequency', 'Single Frequency'])
    
    gmsl_min = float(df['gmsl_gia'].min())
    gmsl_max = float(df['gmsl_gia'].max())
    gmsl_range = st.slider("Sea Level Range (mm)", gmsl_min, gmsl_max, (gmsl_min, gmsl_max))
    
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
    st.markdown(f"""<div class="metric-item rose"><div class="metric-label">Total Records</div>
        <div class="metric-value">{len(filtered_df):,}</div><div class="metric-sub">measurements filtered</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-item blush"><div class="metric-label">Peak Sea Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].max():.1f}<span style="font-size:1rem">mm</span></div><div class="metric-sub">highest recorded</div></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-item mauve"><div class="metric-label">Average Level</div>
        <div class="metric-value">{filtered_df['gmsl_gia'].mean():.1f}<span style="font-size:1rem">mm</span></div><div class="metric-sub">mean variation</div></div>""", unsafe_allow_html=True)
with m4:
    total_rise = filtered_df['gmsl_gia'].max() - filtered_df['gmsl_gia'].min()
    st.markdown(f"""<div class="metric-item warm"><div class="metric-label">Total Rise</div>
        <div class="metric-value">{total_rise:.1f}<span style="font-size:1rem">mm</span></div><div class="metric-sub">over selected period</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Distribution", "Trends", "Relationships", "Data Table", "Bonus Charts"])

# ── TAB 1 ──
with tab1:
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">1</span><div><p class="chart-info-title">Altimeter Type Distribution</p><p class="chart-info-desc">Proportional split between dual and single frequency altimeter types</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.pie_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">2</span><div><p class="chart-info-title">Sea Level Variation Distribution</p><p class="chart-info-desc">Frequency histogram of GMSL values across all measurements</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.histogram(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">9</span><div><p class="chart-info-title">Measurements by Altimeter Type</p><p class="chart-info-desc">Count of total readings taken by each altimeter instrument</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.count_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 2 ──
with tab2:
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">3</span><div><p class="chart-info-title">Sea Level Rise Over Time</p><p class="chart-info-desc">Raw and smoothed GMSL from 1993 to 2025 showing clear upward trend</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.line_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">4</span><div><p class="chart-info-title">Average Sea Level by Decade</p><p class="chart-info-desc">Bar comparison of mean sea level values across each decade</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.bar_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">8</span><div><p class="chart-info-title">Cumulative Sea Level Rise</p><p class="chart-info-desc">Area chart showing the total accumulated rise over the entire period</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.area_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 3 ──
with tab3:
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">5</span><div><p class="chart-info-title">GIA vs Non-GIA Measurements</p><p class="chart-info-desc">Scatter relationship between corrected and uncorrected sea level readings</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.scatter_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">6</span><div><p class="chart-info-title">Sea Level Distribution by Era</p><p class="chart-info-desc">Box plot showing spread, median and outliers per era</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.box_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">7</span><div><p class="chart-info-title">Feature Correlation Heatmap</p><p class="chart-info-desc">Correlation matrix between all sea level measurement variables</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.heatmap(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">10</span><div><p class="chart-info-title">Sea Level Density by Era</p><p class="chart-info-desc">Violin plot showing probability density of sea level per era</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.violin_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4 ──
with tab4:
    display_cols = ['year', 'era', 'gmsl_gia', 'smooth_gia', 'std_gia', 'altimeter_label', 'num_observations']
    st.dataframe(filtered_df[display_cols].round(2), use_container_width=True, height=450)
    st.markdown('<br>', unsafe_allow_html=True)
    st.dataframe(filtered_df[['gmsl_gia', 'smooth_gia', 'std_gia']].describe().round(2), use_container_width=True)

# ── TAB 5 ──
with tab5:
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">+</span><div><p class="chart-info-title">Pair Plot — Sea Level Features</p><p class="chart-info-desc">Relationships between all sea level measurement variables combined</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.pair_plot(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">+</span><div><p class="chart-info-title">Bubble Chart — Sea Level by Decade</p><p class="chart-info-desc">Bubble size = total observations. Color intensity = sea level rise.</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.bubble_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card"><div class="chart-card-header"><span class="chart-num">+</span><div><p class="chart-info-title">Funnel Chart — Measurements by Era</p><p class="chart-info-desc">Distribution of total satellite measurements across time eras</p></div></div>', unsafe_allow_html=True)
    st.pyplot(charts.funnel_chart(filtered_df), transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)