import pandas as pd 
from config import *
from qc import quality_control, filtering

station = "mitilini"
"""-----ΑΝΑΓΝΩΣΗ ΑΡΧΕΙΩΝ-----"""
df_1 = pd.read_excel(mitilini_path_1, decimal=",")
df_2= pd.read_csv(mitilini_path_2, sep= ";", usecols=range(1,16))
df_3= pd.read_csv(mitilini_path_3, sep= ";",usecols=range(2,12))
df_4 = pd.read_excel(mitilini_path_4,decimal=",",usecols=range(5),skiprows=6)
df_5 = pd.read_excel(mitilini_path_5,decimal=",",usecols=range(10), skiprows=11)
df_6 = pd.read_excel(mitilini_path_6,decimal=",",usecols=[1,3,5,6,10],skiprows=8)
df_7 = pd.read_excel(mitilini_path_7,decimal=",",usecols=[1,3,5,6,10],skiprows=8)
df_8 = pd.read_excel(mitilini_path_8,decimal=",",usecols=[1,3,5,6,10],skiprows=8)
df_9 = pd.read_excel(mitilini_path_9,decimal=",",usecols=[1,3,5,6,10],skiprows=8)
df_10 = pd.read_excel(mitilini_path_10,decimal=",",usecols=[1,3,5,6,10],skiprows=8)


"""-----ΜΕΤΟΝΟΜΑΣΙΑ (ΒΑΣΕΙ ΑΡΧΕΙΟΥ CONFIG)-----"""

dfs= [df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10]
maps= [rename_map1, rename_map2, rename_map3, rename_map4, rename_map5, rename_map6_10, rename_map6_10, rename_map6_10, rename_map6_10, rename_map6_10]

for df, map in zip(dfs, maps):
    df.rename(columns=map, inplace=True)


"""-----ΜΟΡΦΟΠΟΙΗΣΗ ΗΜΕΡΟΜΗΝΙΑΣ-----"""

for df in dfs:  
    df["UTC"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour"]], errors='coerce')
    df.drop(["Year", "Month", "Day", "Hour"], axis=1, inplace=True)
    df.set_index("UTC", inplace=True)
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)


"""-----ΣΥΓΧΩΝΕΥΣΗ-----"""

def combine(*dfs):

    df = pd.concat(dfs)
    df = df.groupby('UTC', as_index=True).first()
    df.sort_index(inplace=True)
    return df

cdf = combine(df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10).copy()

   

"""-----QUALITY CONTROL & FILTERING-----"""

for col in cdf.columns:
    cdf[col] = pd.to_numeric(cdf[col], errors="coerce") 
    cdf[col] = cdf[col].where(cdf[col] <= 1e6)  # INITIAL SCREENING
df= cdf.copy()
qcdf = quality_control(cdf, limdictmitilini, errdictmitilini)
# qcdf.to_csv(qcpath + f"_{station}.csv")
fdf = filtering(qcdf).copy()


pct_raw = ((df.count() / len(df)) * 100).round(2).rename('Validity Raw (%)')

notqccols = [col for col in qcdf.columns if 'QC' not in col]
pctdf = qcdf[notqccols].copy() 
pct_filtered = ((pctdf.count() / len(pctdf)) * 100).round(2).rename('Validity Filtered (%)')


validity_df = pd.concat([pct_raw, pct_filtered], axis=1).reset_index()
validity_df['dropped from QC'] = validity_df['Validity Raw (%)'] - validity_df['Validity Filtered (%)']
validity_df.rename(columns={'index': 'Column'}, inplace=True)
validity_df.to_csv(os.path.join(dataframes_dir, station, f'validity_percentage_{station}.csv'), index=False)
fdf.to_csv(os.path.join(dataframes_dir, station, f"filtered_{station}.csv"))
