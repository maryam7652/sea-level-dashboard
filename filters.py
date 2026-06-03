import pandas as pd
import numpy as np
import os

def load_data():
    possible_paths = [
        'GMSL_TPJAOS_5.2.txt',
        'data/GMSL_TPJAOS_5.2.txt',
        r'C:\Users\HP\Documents\GMSL_TPJAOS_5_2.txt'
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path, comment='H', sep=r'\s+', header=None)
            break
    
    if df is None:
        df = pd.read_csv(r'C:\Users\HP\Documents\GMSL_TPJAOS_5_2.txt',
                         comment='H', sep=r'\s+', header=None)

    df.columns = ['altimeter_type', 'cycle_number', 'year',
                  'num_observations', 'num_weighted_obs',
                  'gmsl_no_gia', 'std_no_gia', 'smooth_no_gia',
                  'gmsl_gia', 'std_gia', 'smooth_gia',
                  'smooth_gia_no_seasonal', 'smooth_no_gia_no_seasonal']

    df = df.replace(99900.000, np.nan)
    df['decade'] = (df['year'].astype(int) // 10) * 10
    df['era'] = pd.cut(df['year'],
                       bins=[1992, 2000, 2010, 2020, 2026],
                       labels=['1990s', '2000s', '2010s', '2020s'])
    df['altimeter_label'] = df['altimeter_type'].apply(
        lambda x: 'Dual Frequency' if x == 0 else 'Single Frequency')

    return df

def apply_filters(df, year_range, era, altimeter, gmsl_range, search):
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    if era != 'All':
        df = df[df['era'] == era]
    if altimeter != 'All':
        df = df[df['altimeter_label'] == altimeter]
    df = df[(df['gmsl_gia'] >= gmsl_range[0]) & (df['gmsl_gia'] <= gmsl_range[1])]
    if search:
        df = df[df['year'].astype(str).str.contains(search, na=False)]
    return df