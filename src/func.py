import pandas as pd

def get_data():
    df = pd.read_excel("PATH_TO_FILE")
    return df

def get_top_five_yielders(df, checks = []):
    df['Marketable Yield'] = df[['A1', 'A2', 'A3', 'A4']].sum(axis=1, skipna = True)
    yieldByClone = df.groupby('Clone', as_index = False)['Marketable Yield'].mean()
    return yieldByClone.sort_values(['Marketable Yield'], ignore_index = True, ascending = False)

def get_progress(df):
    numberDone = df['Timestamp'].count()
    total = len(df)
    return(f'{numberDone}/{total}')

def get_current_plot(df):
    latest_plot_row = df[df['Timestamp'] == df['Timestamp'].max()]
    return latest_plot_row['Plot'].iloc[0]


