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
    filtered = df.copy()

    # 1. Year Range Filter (Slider)
    filtered = filtered[(filtered['year'] >= year_range[0]) & (filtered['year'] <= year_range[1])]

    # 2. Multi-Select Filter (Era Requirement)
    if era: # As long as the user hasn't un-checked every box
        filtered = filtered[filtered['era'].isin(era)]
    else:
        # If they clear the multi-select completely, show no data
        filtered = filtered[filtered['era'].isin([])]

    # 3. Category Filter Dropdown (Altimeter)
    if altimeter != 'All':
        filtered = filtered[filtered['altimeter_label'] == altimeter]

    # 4. Numerical Range Filter
    filtered = filtered[(filtered['gmsl_gia'] >= gmsl_range[0]) & (filtered['gmsl_gia'] <= gmsl_range[1])]

    # 5. Search / Text Filter
    if search:
        # Check if the search text is inside the year string
        filtered = filtered[filtered['year'].astype(str).str.contains(search, case=False, na=False)]

    return filtered