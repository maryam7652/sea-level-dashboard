import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def pie_chart(df):
    fig, ax = plt.subplots(figsize=(7,7))
    counts = df['altimeter_label'].value_counts()
    if counts.empty:
        ax.text(0.5, 0.5, 'No data', ha='center')
    else:
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%',
               colors=['#4facfe', '#f093fb'], startangle=90)
    ax.set_title('Altimeter Type Distribution', fontsize=14, fontweight='bold')
    return fig

def histogram(df):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(df['gmsl_gia'].dropna(), bins=30, color='steelblue', edgecolor='black')
    ax.set_title('Distribution of Sea Level Variations', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sea Level Variation (mm)')
    ax.set_ylabel('Frequency')
    return fig

def line_chart(df):
    fig, ax = plt.subplots(figsize=(14,5))
    ax.plot(df['year'], df['gmsl_gia'], color='royalblue', alpha=0.4, linewidth=0.8)
    ax.plot(df['year'], df['smooth_gia'], color='red', linewidth=2, label='Smoothed')
    ax.set_title('Global Mean Sea Level Rise Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    ax.legend()
    ax.grid(True)
    return fig

def bar_chart(df):
    fig, ax = plt.subplots(figsize=(10,5))
    decade_avg = df.groupby('decade')['gmsl_gia'].mean().reset_index()
    sns.barplot(data=decade_avg, x='decade', y='gmsl_gia',
                hue='decade', palette='viridis', legend=False, ax=ax)
    ax.set_title('Average Sea Level by Decade', fontsize=14, fontweight='bold')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    return fig

def scatter_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sample = df.sample(min(500, len(df)), random_state=42)
    ax.scatter(sample['gmsl_no_gia'], sample['gmsl_gia'], alpha=0.3, color='steelblue', s=5)
    ax.set_title('GMSL with GIA vs without GIA', fontsize=14, fontweight='bold')
    ax.set_xlabel('GMSL without GIA (mm)')
    ax.set_ylabel('GMSL with GIA (mm)')
    ax.grid(True)
    return fig

def box_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    if filtered.empty:
        ax.text(0.5, 0.5, 'No data', ha='center')
    else:
        sns.boxplot(data=filtered, x='era', y='gmsl_gia',
                    hue='era', palette='Set2', legend=False, ax=ax)
    ax.set_title('Sea Level Distribution by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(10,8))
    corr = df[['gmsl_no_gia', 'gmsl_gia', 'smooth_gia',
               'smooth_no_gia', 'std_gia', 'num_observations']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1, ax=ax)
    ax.set_title('Correlation Heatmap of Sea Level Features', fontsize=14, fontweight='bold')
    return fig

def area_chart(df):
    fig, ax = plt.subplots(figsize=(14,5))
    ax.fill_between(df['year'], df['smooth_gia'], alpha=0.4, color='royalblue')
    ax.plot(df['year'], df['smooth_gia'], color='royalblue', linewidth=1.5)
    ax.set_title('Cumulative Sea Level Rise Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level Variation (mm)')
    ax.grid(True)
    return fig

def count_plot(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=df, x='altimeter_label',
                  hue='altimeter_label', palette='pastel', legend=False, ax=ax)
    ax.set_title('Count of Measurements by Altimeter Type', fontsize=14, fontweight='bold')
    ax.set_xlabel('Altimeter Type')
    ax.set_ylabel('Count')
    return fig

def violin_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    filtered = df.dropna(subset=['era', 'gmsl_gia'])
    sns.violinplot(data=filtered, x='era', y='gmsl_gia',
                   hue='era', palette='muted', legend=False, ax=ax)
    ax.set_title('Sea Level Distribution by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Era')
    ax.set_ylabel('Sea Level Variation (mm)')
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
        alpha=0.7,
        edgecolors='black'
    )
    for _, row in decade_stats.iterrows():
        ax.annotate(f"{int(row['decade'])}s",
                    (row['decade'], row['avg_sea_level']),
                    textcoords='offset points',
                    xytext=(0,10), ha='center', fontsize=9)
    plt.colorbar(scatter, ax=ax, label='Avg Sea Level (mm)')
    ax.set_title('Bubble Chart - Sea Level by Decade', fontsize=14, fontweight='bold')
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average Sea Level Variation (mm)')
    ax.grid(True, alpha=0.3)
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
                f'{val:,}', va='center', fontsize=10)
    ax.set_title('Sea Level Measurements by Era', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Measurements')
    ax.invert_yaxis()
    return fig

def pair_plot(df):
    sample = df[['gmsl_gia', 'gmsl_no_gia', 'smooth_gia', 'std_gia']].dropna().sample(
        min(500, len(df)), random_state=42)
    pg = sns.pairplot(sample, plot_kws={'alpha': 0.3})
    pg.fig.suptitle('Pair Plot - Sea Level Features', y=1.02, fontsize=14, fontweight='bold')
    return pg.fig