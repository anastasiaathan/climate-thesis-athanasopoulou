import pandas as pd
import csv
import os
import warnings
from config import *
from qc import quality_control, filtering
warnings.simplefilter(action='ignore', category=FutureWarning)

station= "sigri"
'''-----ΔΙΑΧΩΡΙΣΜΟΣ ΔΕΔΟΜΕΝΩΝ ΣΕ 10 ΚΑΙ 60 ΛΕΠΤΑ ΚΑΙ ΜΕΤΟΝΟΜΑΣΙΑ ------'''

def sigri_data1(filepath):
    df=pd.read_csv(filepath, header=None, sep=',', decimal='.',usecols=range(0,31))
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df_110 = df[df[0] == 110].copy() 
    df_160 = df[df[0] == 160].copy() 
    df_110=df_110.drop(columns=[30]) 
    df_110.columns = sigriheader110
    df_160.columns = sigriheader160
    fix_datetime(df_110)
    fix_datetime(df_160)
    return df_110,df_160

    
def sigri_data3(filepath):
    df=pd.read_csv(filepath, header=None, skiprows=45033, sep=',', decimal='.',usecols=range(0,31))
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df_110 = df[df[0] == 110].copy()
    df_160 = df[df[0] == 160].copy()
    df_110=df_110.drop(columns=[30]) 
    df_110.columns = sigriheader110
    df_160.columns = sigriheader160
    fix_datetime(df_110)
    fix_datetime(df_160)
    return df_110,df_160

def sigri_data24(filepath): 
    rows_110 = []
    rows_160 = []
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if not row or len(row) < 1:
                continue
            try:
                frequency_code = int(row[0]) 
            except ValueError:
                continue
            if frequency_code == 110:
                rows_110.append(row[:30])
            elif frequency_code == 160:
                rows_160.append(row[:31])
    df_110 = pd.DataFrame(rows_110)
    df_160 = pd.DataFrame(rows_160)
    for df_target in [df_110, df_160]:
        for col in df_target.columns:
            df_target[col] = pd.to_numeric(df_target[col], errors="coerce")
    df_110.columns = sigriheader110
    df_160.columns = sigriheader160
    fix_datetime(df_110)
    fix_datetime(df_160)
    return df_110,df_160

'''-----ΜΟΡΦΟΠΟΙΗΣΗ ΗΜΕΡΟΜΗΝΙΑΣ-----'''

def fix_datetime(df): 
    df['Hour'] = df['Hour/Min'] // 100 
    df['Minute'] = df['Hour/Min'] % 100
    df['UTC'] = pd.to_datetime({'year': df['Year'], 'month': 1, 'day': 1}) + pd.to_timedelta(df['Day'] - 1, unit='D') + pd.to_timedelta(df['Hour'], unit='h') + pd.to_timedelta(df['Minute'], unit='m')
    df.drop(columns=['Hour', 'Minute'], inplace=True)

'''-----ΣΥΓΧΩΝΕΥΣΗ-----'''

def combine(*dfs):
    df = pd.concat(dfs)
    df = df.groupby('UTC', as_index=True).first()
    df.sort_index(inplace=True)
    return df

'''-----RESAMPLING 10 ΛΕΠΤΩΝ ΓΙΑ ΣΥΓΚΡΙΣΗ ΜΕ 60ΛΕΠΤΑ-----'''

def resample(path): 
    cdf=pd.read_csv(path)
    cdf['UTC'] = pd.to_datetime(cdf['UTC'], format='ISO8601')
    cdf.set_index('UTC', inplace=True)
    df= cdf.resample('60min').agg(aggdictsigri110)
    df.to_csv (os.path.join(dataframes_dir, station, "resampled_10min_to_hourly_for_comparison_df.csv"))
    return df

'''-----PREPROCESSING-----'''

df1_110, df1_160 = sigri_data1(file1path)  
df3_110, df3_160 = sigri_data3(file3path) 
df2_110, df2_160 = sigri_data24(file2path)
df4_110, df4_160 = sigri_data24(file4path)
df110= combine(df1_110,df2_110,df3_110,df4_110).copy()
df110 = df110.resample('60min').agg(aggdictsigri110).copy()
df110.to_csv(df110path)
df160= combine(df1_160,df2_160,df3_160,df4_160).copy()

df160.to_csv(df160path)


'''-----QUALITY CONTROL AND FILTERING-----'''

'''-----Quality control-----'''
df160 = pd.read_csv(df160path)
df160= df160.drop(columns=['Frequency','StnCode','Year','Day','Hour/Min']).copy()
df160['UTC'] = pd.to_datetime(df160['UTC'], format='ISO8601')
df160.set_index('UTC', inplace=True)
df= df160.copy()
qcdf = quality_control(df160,limdictsigri, errdictsigri)

fdf=filtering(qcdf).copy()
fdf.to_csv(os.path.join(dataframes_dir, station, f"filtered_{station}.csv"))



pct_raw = ((df.count() / len(df)) * 100).round(2).rename('Validity Raw (%)')

notqccols = [col for col in qcdf.columns if 'QC' not in col]
pctdf = fdf[notqccols].copy() 
pct_filtered = ((pctdf.count() / len(pctdf)) * 100).round(2).rename('Validity Filtered (%)')


validity_df = pd.concat([pct_raw, pct_filtered], axis=1).reset_index()
validity_df['dropped from QC'] = (validity_df['Validity Raw (%)'] - validity_df['Validity Filtered (%)']).round(2)
validity_df.rename(columns={'index': 'Column'}, inplace=True)
validity_df.to_csv(os.path.join(dataframes_dir, station, f'validity_percentage_{station}.csv'), index=False)
fdf.to_csv(os.path.join(dataframes_dir, station, f"filtered_{station}.csv"))


