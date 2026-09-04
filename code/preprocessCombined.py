import pandas as pd 
from config import *
import matplotlib.pyplot as plt
from plotting import plotcols, plot_gaussians_by_location
stations = ['mitilini', 'sigri']
mitilini_path= os.path.join(dataframes_dir, "mitilini", "filtered_mitilini.csv")
sigri_path = os.path.join(dataframes_dir, "sigri", "filtered_sigri.csv")

mitilini_df= pd.read_csv(mitilini_path)
sigri_df= pd.read_csv(sigri_path) 

sigri_df['WS (knots)'] = sigri_df['WS(m per s)'] * 1.94384
dfs = [mitilini_df, sigri_df]
aggdicts = [aggdictmitilini, aggdict160combined]
locations = ['Mitilini', 'Sigri']

processed_dfs = []
for df,aggdict,location in zip(dfs, aggdicts, locations):
    df['UTC']= pd.to_datetime(df['UTC'], format= 'ISO8601')
    df.set_index('UTC', inplace=True)
    df = df.resample('ME').agg(aggdict).copy()
    df['Location']= location
    processed_dfs.append(df)

df_combined = pd.concat(processed_dfs, keys=locations, names=['Location', 'UTC'])
df_combined = df_combined.reorder_levels(['UTC', 'Location']).sort_index()
start_date = max(df.index.min() for df in processed_dfs)
end_date = min(df.index.max() for df in processed_dfs)
df_combined = df_combined.loc[start_date:end_date].copy()
validity_series = (df_combined.notnull().mean() * 100).astype(int)
validitydf = validity_series.reset_index()
validitydf.columns = ['Column', 'ValidityPercentage (%)']
validitydf.to_csv(os.path.join(dataframes_dir, "combined", 'validity_percentage_combined.csv'), index=False)
df_combined.to_csv(os.path.join(dataframes_dir, "combined", 'filtered_combined.csv'), index=False) 

