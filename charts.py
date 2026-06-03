import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as pe
import seaborn as sns
import numpy as np

# ── THEME HELPER ──────────────────────────────────────────────────
# A soft, elegant neutral palette to contrast against the full pink UI
NEUTRAL_PALETTE = ["#0ea5e9", "#8b5cf6", "#f59e0b", "#10b981", "#6366f1", "#ec4899"]

# The magic text outline that makes text readable on ANY background
OUTLINE = [pe.withStroke(linewidth=2.5, foreground='white')]
TEXT_COLOR = "#4c0519" # Deep Maroon

def _base_fig(w=10, h=5):
    """Return a figure + axes with transparent bg and high-contrast glowing text."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_alpha(0.0)          
    ax.set_facecolor("none")          
    
    # Style Ticks
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_path_effects(OUTLINE)
        label.set_fontweight('bold')
        
    # Style Spines (Borders) using Matplotlib-safe hex alpha (#f43f5e40 = 25% opacity)
    for spine in ax.spines.values():
        spine.set_edgecolor("#f43f5e40")
        
    # Style Titles and Axes Labels
    ax.title.set_color(TEXT_COLOR)
    ax.title.set_path_effects(OUTLINE)
    ax.title.set_fontweight('bold')
    ax.title.set_fontsize(14)
    
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.xaxis.label.set_path_effects(OUTLINE)
    ax.xaxis.label.set_fontweight('bold')
    ax.xaxis.label.set_fontsize(11)
    
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_path_effects(OUTLINE)
    ax.yaxis.label.set_fontweight('bold')
    ax.yaxis.label.set_fontsize(11)
    
    return fig, ax

def _style_ax(ax):
    """Apply consistent grid styling."""
    ax.grid(True, color="#f43f5e26", linewidth=0.7, linestyle="--") # #f43f5e26 = 15% opacity
    ax.set_axisbelow(True)
    return ax

# ── CHARTS ────────────────────────────────────────────────────────

def pie_chart(df):
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")
    counts = df['altimeter_label'].value_counts()
    
    if counts.empty:
        txt = ax.text(0.5, 0.5, 'No data available', ha='center', va='center', color=TEXT_COLOR, fontsize=12, fontweight='bold')
        txt.set_path_effects(OUTLINE)
        ax.axis('off')
    else:
        colors = ["#0ea5e9", "#8b5cf6"]
        wedges, texts, autotexts = ax.pie(
            counts, labels=counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2),
        )
        for t in texts:
            t.set_color(TEXT_COLOR)
            t.set_fontsize(12)
            t.set_fontweight("bold")
            t.set_path_effects(OUTLINE)
        for at in autotexts:
            at.set_color("white")
            at.set_fontsize(11)
            at.set_fontweight("bold")
            
    ax.set_title('Altimeter Type Distribution', fontsize=15, fontweight='bold', color=TEXT_COLOR, pad=12).set_path_effects(OUTLINE)
    return fig

def histogram(df):
    fig, ax = _base_fig(10, 5)
    data = df['gmsl_gia'].dropna()
    n, bins, patches = ax.hist(data, bins=30, color="#0ea5e9", edgecolor='white', linewidth=0.6, alpha=0.85)
    
    norm = mpl.colors.Normalize(vmin=bins.min(), vmax=bins.max())
    cmap = mpl.cm.Blues
    for patch, left in zip(patches, bins[:-1]):
        patch.set_facecolor(cmap(norm(left) * 0.7 + 0.3))
        
    ax.set_title('Distribution of Sea Level Variations')
    ax.set_xlabel('Sea Level Variation (mm)')
    ax.set_ylabel('Frequency')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def line_chart(df):
    fig, ax = _base_fig(14, 5)
    ax.plot(df['year'], df['gmsl_gia'], color="#0ea5e9", alpha=0.45, linewidth=0.9, label='Raw GMSL')
    ax.plot(df['year'], df['smooth_gia'], color="#f59e0b", linewidth=2.5, label='Smoothed', zorder=3)
    ax.fill_between(df['year'], df['gmsl_gia'], alpha=0.06, color="#0ea5e9")
                    
    ax.set_title('Global Mean Sea Level Rise Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    
    legend = ax.legend(framealpha=0.0)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)
        text.set_fontweight('bold')
        text.set_path_effects(OUTLINE)
        
    _style_ax(ax)
    fig.tight_layout()
    return fig

def bar_chart(df):
    fig, ax = _base_fig(10, 5)
    decade_avg = df.groupby('decade')['gmsl_gia'].mean().reset_index()
    bars = ax.bar(decade_avg['decade'].astype(str), decade_avg['gmsl_gia'],
                  color=NEUTRAL_PALETTE[:len(decade_avg)],
                  edgecolor='white', linewidth=0.8, width=0.55)
                  
    for bar in bars:
        h = bar.get_height()
        txt = ax.text(bar.get_x() + bar.get_width() / 2, h + 0.8,
                f'{h:.1f}', ha='center', va='bottom', fontsize=11, color=TEXT_COLOR, fontweight='bold')
        txt.set_path_effects(OUTLINE)
                
    ax.set_title('Average Sea Level by Decade')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def scatter_plot(df):
    fig, ax = _base_fig(10, 6)
    sample = df.sample(min(500, len(df)), random_state=42)
    ax.scatter(sample['gmsl_no_gia'], sample['gmsl_gia'], alpha=0.55, color="#8b5cf6", s=18, edgecolors='none')
                    
    ax.set_title('GMSL with GIA vs without GIA')
    ax.set_xlabel('GMSL without GIA (mm)')
    ax.set_ylabel('GMSL with GIA (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def box_plot(df):
    fig, ax = _base_fig(10, 6)
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    
    if filtered.empty:
        txt = ax.text(0.5, 0.5, 'No data available', ha='center', va='center', color=TEXT_COLOR, fontsize=12, fontweight='bold')
        txt.set_path_effects(OUTLINE)
        ax.axis('off')
    else:
        sns.boxplot(data=filtered, x='era', y='gmsl_gia', hue='era', palette='Set2', legend=False,
                    ax=ax, linewidth=1.2, flierprops=dict(marker='o', markersize=4, markerfacecolor='#aaa', alpha=0.5))
        ax.set_facecolor("none")
        
    ax.set_title('Sea Level Distribution by Era')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")
    corr = df[['gmsl_no_gia', 'gmsl_gia', 'smooth_gia', 'smooth_no_gia', 'std_gia', 'num_observations']].corr()
               
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.8, linecolor='#f43f5e33', # #f43f5e33 = 20% opacity
                annot_kws={"size": 11, "weight": "bold"}, ax=ax)
                
    ax.set_title('Correlation Heatmap of Sea Level Features', fontsize=14, fontweight='bold', color=TEXT_COLOR, pad=12).set_path_effects(OUTLINE)
    
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_path_effects(OUTLINE)
        label.set_fontweight('bold')
        
    fig.tight_layout()
    return fig

def area_chart(df):
    fig, ax = _base_fig(14, 5)
    ax.fill_between(df['year'], df['smooth_gia'], alpha=0.22, color="#0ea5e9")
    ax.plot(df['year'], df['smooth_gia'], color="#0ea5e9", linewidth=2.2)
            
    ax.set_title('Cumulative Sea Level Rise Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def count_plot(df):
    fig, ax = _base_fig(8, 5)
    order = df['altimeter_label'].value_counts().index.tolist()
    
    sns.countplot(data=df, x='altimeter_label', order=order, hue='altimeter_label', palette=NEUTRAL_PALETTE[:2],
                  legend=False, ax=ax, edgecolor='#f43f5e40', linewidth=0.8)
    ax.set_facecolor("none")
    
    ax.set_title('Count of Measurements by Altimeter Type')
    ax.set_xlabel('Altimeter Type')
    ax.set_ylabel('Count')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def violin_plot(df):
    fig, ax = _base_fig(10, 6)
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    
    if not filtered.empty:
        sns.violinplot(data=filtered, x='era', y='gmsl_gia', hue='era', palette='muted', legend=False,
                       ax=ax, linewidth=1.2, inner='quartile')
        ax.set_facecolor("none")
        
    ax.set_title('Sea Level Distribution by Era (Violin)')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def bubble_chart(df):
    fig, ax = _base_fig(12, 6)
    decade_stats = df.groupby('decade').agg(
        avg_sea_level=('gmsl_gia', 'mean'), avg_std=('std_gia', 'mean'), total_obs=('num_observations', 'sum')
    ).reset_index()
    
    scatter = ax.scatter(
        decade_stats['decade'], decade_stats['avg_sea_level'],
        s=decade_stats['total_obs'] / 500000, c=decade_stats['avg_sea_level'],
        cmap='RdYlBu_r', alpha=0.82, edgecolors='#f43f5e40', linewidths=1.5
    )
    
    for _, row in decade_stats.iterrows():
        txt = ax.annotate(f"{int(row['decade'])}s", (row['decade'], row['avg_sea_level']),
                    textcoords='offset points', xytext=(0, 12), ha='center',
                    fontsize=11, fontweight='bold', color=TEXT_COLOR)
        txt.set_path_effects(OUTLINE)
                    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Avg Sea Level (mm)', color=TEXT_COLOR, fontweight='bold')
    cbar.ax.yaxis.label.set_path_effects(OUTLINE)
    cbar.ax.yaxis.set_tick_params(colors=TEXT_COLOR)
    for label in cbar.ax.yaxis.get_ticklabels():
        label.set_fontweight('bold')
        label.set_path_effects(OUTLINE)
        
    cbar.outline.set_edgecolor('#f43f5e40')
    
    ax.set_title('Bubble Chart — Sea Level by Decade')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    _style_ax(ax)
    fig.tight_layout()
    return fig

def funnel_chart(df):
    fig, ax = _base_fig(10, 6)
    stages = {
        'Total Measurements': len(df), '1990s': len(df[df['era'] == '1990s']), '2000s': len(df[df['era'] == '2000s']),
        '2010s': len(df[df['era'] == '2010s']), '2020s': len(df[df['era'] == '2020s']),
    }
    labels = list(stages.keys())
    values = list(stages.values())
    colors = ["#0ea5e9", "#10b981", "#f59e0b", "#f4845f", "#8b5cf6"]
    
    bars = ax.barh(labels, values, color=colors, height=0.52, edgecolor='#f43f5e40', linewidth=0.8)
                   
    for bar, val in zip(bars, values):
        txt = ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                f'{val:,}', va='center', fontsize=11, color=TEXT_COLOR, fontweight='bold')
        txt.set_path_effects(OUTLINE)
                
    ax.set_title('Sea Level Measurements by Era')
    ax.set_xlabel('Number of Measurements')
    ax.invert_yaxis()
    _style_ax(ax)
    fig.tight_layout()
    return fig

def pair_plot(df):
    sample = df[['gmsl_gia', 'gmsl_no_gia', 'smooth_gia', 'std_gia']].dropna().sample(min(500, len(df)), random_state=42)
        
    pg = sns.pairplot(
        sample, plot_kws={'alpha': 0.45, 'color': '#0ea5e9', 's': 12}, diag_kws={'color': '#0ea5e9', 'alpha': 0.7}
    )
    pg.fig.patch.set_alpha(0.0)
    
    for ax in pg.axes.flatten():
        if ax:
            ax.set_facecolor("none")
            for spine in ax.spines.values():
                spine.set_edgecolor("#f43f5e40")
            ax.tick_params(colors=TEXT_COLOR, labelsize=9)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_path_effects(OUTLINE)
                label.set_fontweight('bold')
                
            if ax.xaxis.label:
                ax.xaxis.label.set_color(TEXT_COLOR)
                ax.xaxis.label.set_path_effects(OUTLINE)
                ax.xaxis.label.set_fontweight('bold')
            if ax.yaxis.label:
                ax.yaxis.label.set_color(TEXT_COLOR)
                ax.yaxis.label.set_path_effects(OUTLINE)
                ax.yaxis.label.set_fontweight('bold')
            
    suptitle = pg.fig.suptitle('Pair Plot — Sea Level Features', y=1.02, fontsize=15, fontweight='bold', color=TEXT_COLOR)
    suptitle.set_path_effects(OUTLINE)
    return pg.fig