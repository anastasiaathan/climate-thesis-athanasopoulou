import scipy.stats as stats
import numpy as np
import pandas as pd
from config import * 

def quality_control(df, limdict,errdict):
    for col in df.columns:
        df[f'QC_{col}'] = ''
        
        df[f'QC_{col}'] = df[f'QC_{col}'] + np.where(df[col].isna(), '0', '1') # FLAGS MISSING VALUES
        
        within_limits = (df[col] >= limdict[col]['min']) & (df[col] <= limdict[col]['max']) # FLAGS PHYSICAL LIMITS
        
        df[f'QC_{col}'] = df[f'QC_{col}'] + np.where(within_limits, '1', '0')
        
        z_scores = np.abs(stats.zscore(df[col], nan_policy='omit')) # FLAGS OUTLIERS Z>4
        df[f'QC_{col}'] = df[f'QC_{col}'] + np.where(z_scores < 4, '1', '0')
        
        found_err = (df[col] == errdict[col] if col in errdict else False) # FLAGS ERROR VALUES
        df[f'QC_{col}'] =df[f'QC_{col}'] + np.where(found_err, '0', '1') # FLAGS ERROR VALUES


        
    return df

def filtering(df):
    datacols= [col for col in df.columns if "QC" not in col]
    for col in datacols:
        df[col] = np.where(df[f'QC_{col}'] == '1111', df[col], np.nan)
        #DROP THE OTHER COLUMNS TO MAKE THE PLOTS, OR CHANGE THE WAY YOU HAVE THE PLOTS MADE
    return df
