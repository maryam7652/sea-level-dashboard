import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def _apply_dark_transparent_theme(fig, ax=None):
    """
    Helper function to strip out white backgrounds and turn text white 
    so the charts blend perfectly with the dark dashboard CSS.
    """
    fig.patch.set_facecolor('none')  # Make outer figure transparent
    
    # Grab all axes in the figure (handles both single plots and grid plots)
    axes = fig.axes if ax is None else ([ax] if not isinstance(ax, (list, np.ndarray)) else ax.flatten())
    
    for a in axes:
        a.set_facecolor('none')  # Make inner plot transparent
        a.tick_params(colors='white', labelcolor='white') # Make tick marks & numbers white
        a.xaxis.label.set_color('white') # X-axis label
        a.yaxis.label.set_color('white') # Y-axis label
        a.title.set_color('white')       # Title
        
        # Soften the bounding box lines so they aren't harsh black
        for spine in a.spines.values():
            spine.set_color('rgba(255, 255, 255, 0.2)')


def pie_chart(df):
    fig, ax = plt.subplots(figsize=(7,7))
    counts = df['altimeter_label'].value_counts()
    if counts.empty:
        ax.text(0.5, 0.5, 'No data', ha='center', color='white')
    else:
        # Added textprops to ensure percentage text is white
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%',
               colors=['#4facfe', '#f093fb'], startangle=90, 
               textprops={'color': 'white', 'fontweight': 'bold'})
    
    ax.set_title('Altimeter Type Distribution', fontsize=14, fontweight='bold')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def histogram(df):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(df['gmsl_gia'].dropna(), bins=30, color='steelblue', edgecolor='white')
    ax.set_title('Distribution of Sea Level Variations', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sea Level Variation (mm)')
    ax.set_ylabel('Frequency')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def line_chart(df):
    fig, ax = plt.subplots(figsize=(14,5))
    ax.plot(df['year'], df['gmsl_gia'], color='royalblue', alpha=0.6, linewidth=0.8)
    ax.plot(df['year'], df['smooth_gia'], color='#ff4d4d', linewidth=2.5, label='Smoothed')
    ax.set_title('Global Mean Sea Level Rise Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    
    legend = ax.legend(facecolor='#051525', edgecolor='rgba(255,255,255,0.2)')
    for text in legend.get_texts():
        text.set_color("white")
        
    ax.grid(True, color='rgba(255,255,255,0.1)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def bar_chart(df):
    fig, ax = plt.subplots(figsize=(10,5))
    decade_avg = df.groupby('decade')['gmsl_gia'].mean().reset_index()
    sns.barplot(data=decade_avg, x='decade', y='gmsl_gia',
                hue='decade', palette='viridis', legend=False, ax=ax)
    ax.set_title('Average Sea Level by Decade', fontsize=14, fontweight='bold')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def scatter_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sample = df.sample(min(500, len(df)), random_state=42)
    ax.scatter(sample['gmsl_no_gia'], sample['gmsl_gia'], alpha=0.5, color='#00ccff', s=15)
    ax.set_title('GMSL with GIA vs without GIA', fontsize=14, fontweight='bold')
    ax.set_xlabel('GMSL without GIA (mm)')
    ax.set_ylabel('GMSL with GIA (mm)')
    ax.grid(True, color='rgba(255,255,255,0.1)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def box_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    if filtered.empty:
        ax.text(0.5, 0.5, 'No data', ha='center', color='white')
    else:
        sns.boxplot(data=filtered, x='era', y='gmsl_gia',
                    hue='era', palette='Set2', legend=False, ax=ax)
    ax.set_title('Sea Level Distribution by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(10,8))
    corr = df[['gmsl_no_gia', 'gmsl_gia', 'smooth_gia',
               'smooth_no_gia', 'std_gia', 'num_observations']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1, 
                linecolor='#051525', ax=ax)
    ax.set_title('Correlation Heatmap of Sea Level Features', fontsize=14, fontweight='bold')
    _apply_dark_transparent_theme(fig, ax)
    
    # Fix colorbar text color
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors='white')
    return fig

def area_chart(df):
    fig, ax = plt.subplots(figsize=(14,5))
    ax.fill_between(df['year'], df['smooth_gia'], alpha=0.3, color='#00ccff')
    ax.plot(df['year'], df['smooth_gia'], color='#00ccff', linewidth=2)
    ax.set_title('Cumulative Sea Level Rise Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    ax.grid(True, color='rgba(255,255,255,0.1)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def count_plot(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=df, x='altimeter_label',
                  hue='altimeter_label', palette='pastel', legend=False, ax=ax)
    ax.set_title('Count of Measurements by Altimeter Type', fontsize=14, fontweight='bold')
    ax.set_xlabel('Altimeter Type')
    ax.set_ylabel('Count')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def violin_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    sns.violinplot(data=filtered, x='era', y='gmsl_gia',
                   hue='era', palette='muted', legend=False, ax=ax)
    ax.set_title('Sea Level Distribution by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def bubble_chart(df):
    fig, ax = plt.subplots(figsize=(12,6))
    decade_stats = df.groupby('decade').agg(
        avg_sea_level=('gmsl_gia', 'mean'),
        avg_std=('std_gia', 'mean'),
        total_obs=('num_observations', 'sum')
    ).reset_index()
    scatter = ax.scatter(
        decade_stats['decade'],
        decade_stats['avg_sea_level'],
        s=decade_stats['total_obs'] / 500000,
        c=decade_stats['avg_sea_level'],
        cmap='RdYlBu_r',
        alpha=0.8,
        edgecolors='white'
    )
    for _, row in decade_stats.iterrows():
        ax.annotate(f"{int(row['decade'])}s",
                    (row['decade'], row['avg_sea_level']),
                    textcoords='offset points',
                    xytext=(0,10), ha='center', fontsize=9, color='white', fontweight='bold')
        
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Avg Sea Level (mm)', color='white')
    cbar.ax.tick_params(colors='white')
    
    ax.set_title('Bubble Chart - Sea Level by Decade', fontsize=14, fontweight='bold')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    ax.grid(True, color='rgba(255,255,255,0.1)')
    _apply_dark_transparent_theme(fig, ax)
    return fig

def funnel_chart(df):
    fig, ax = plt.subplots(figsize=(10,6))
    stages = {
        'Total Measurements': len(df),
        '1990s Measurements': len(df[df['era'] == '1990s']),
        '2000s Measurements': len(df[df['era'] == '2000s']),
        '2010s Measurements': len(df[df['era'] == '2010s']),
        '2020s Measurements': len(df[df['era'] == '2020s'])
    }
    labels = list(stages.keys())
    values = list(stages.values())
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
    bars = ax.barh(labels, values, color=colors, edgecolor='white', height=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{val:,}', va='center', fontsize=10, color='white')
        
    ax.set_title('Sea Level Measurements by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Measurements')
    ax.invert_yaxis()
    _apply_dark_transparent_theme(fig, ax)
    return fig

def pair_plot(df):
    sample = df[['gmsl_gia', 'gmsl_no_gia', 'smooth_gia', 'std_gia']].dropna().sample(
        min(500, len(df)), random_state=42)
    pg = sns.pairplot(sample, plot_kws={'alpha': 0.5, 'color': '#00ccff'})
    pg.fig.suptitle('Pair Plot - Sea Level Features', y=1.02, fontsize=14, fontweight='bold', color='white')
    
    # Apply theme across the entire grid of subplots
    _apply_dark_transparent_theme(pg.fig)
    return pg.fig