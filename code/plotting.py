import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import statsmodels.api as sm
import calendar
cwd = os.getcwd()
from config import *

def plotcols(df, usecols, frequency):
    if frequency == 'Y':
        resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    elif frequency == 'Q':
        resampled = df.resample('QE-FEB').agg(aggdict)
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")
        print(resampled.head())
    for col in usecols:
        plt.figure(figsize=(10, 6))
        plt.plot(resampled.index, resampled[col])
        plt.xlabel("UTC")
        unit = unitdict.get(col)
        if unit is not None: 
            plt.ylabel(f"{col} ({unit})")
        else: 
            plt.ylabel(f"{col}")
        plt.title(f"{col} Over Time")
        plt.grid(True)
        plt.tight_layout()
        os.makedirs(os.path.join(plots_dir, "data"), exist_ok=True)
        out_path = os.path.join(plots_dir, "data", f"{col}_{frequency}.png")
        plt.savefig(out_path)
        plt.close()

'''-----PLOTTING 1 GAUSSIAN-----'''
def plot1gaussian(df,col, period_start, period_end):
    # GAUSS
    temp = df[ (df.index >= period_start) & (df.index <= period_end)]

    mean, std = temp[col].mean(), temp[col].std()

    min_val = temp[col].min()
    max_val = temp[col].max()   
    x = np.linspace(min_val - 5, max_val + 5, 200)
    pdf = stats.norm.pdf(x, mean, std)


    plt.figure(figsize=(10, 6))
    plt.plot(x, pdf, 'b-', linewidth=2, label=f'Period {period_start.year} to {period_end.year}: $\\mu={mean:.1f}, \\sigma={std:.1f}$')
    plt.fill_between(x, pdf, color='blue', alpha=0.1) 
    if col == 'TairAv':
        col = 'Mean Temperature'
    plt.xlabel(f"{col} (C)")
    plt.ylabel("Probability Density")
    plt.title(f"{col} Distribution")
    plt.legend()
    plt.tight_layout()
    
    out_path = os.path.join(plots_dir, f"{col}_distributions_{period_start}_{period_end}_vs_{period_start}_{period_end}.png")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(gausspath, f"{col}_gaussian.png"))
    plt.close() 


'''-----PLOTTING 2 GAUSSIANS-----'''

def plot2gaussians(df,col, period1_start, period1_end, period2_start, period2_end):
    # GAUSS
    temp1 = df[ (df.index >= period1_start) & (df.index <= period1_end)]
    temp2 = df[(df.index >= period2_start) & (df.index <= period2_end)]
    mean1, std1 = temp1[col].mean(), temp1[col].std()
    mean2, std2 = temp2[col].mean(), temp2[col].std()
    min_val = min(temp1[col].min(), temp2[col].min())
    max_val = max(temp1[col].max(), temp2[col].max())   
    x = np.linspace(min_val - 5, max_val + 5, 200)
    pdf1 = stats.norm.pdf(x, mean1, std1)
    pdf2 = stats.norm.pdf(x, mean2, std2)

    plt.figure(figsize=(10, 6))
    plt.plot(x, pdf1, 'b-', linewidth=2, label=f'Period {period1_start} to {period1_end}: $\\mu={mean1:.1f}, \\sigma={std1:.1f}$')
    plt.plot(x, pdf2, 'r-', linewidth=2, label=f'Period {period2_start} to {period2_end}: $\\mu={mean2:.1f}, \\sigma={std2:.1f}$')
    plt.fill_between(x, pdf1, color='blue', alpha=0.1) 
    plt.fill_between(x, pdf2, color='red', alpha=0.1) 
    if col == 'TairAv':
        col = 'Mean Temperature'
    plt.xlabel(f"{col} (C)")
    plt.ylabel("Probability Density")
    plt.title(f"{col} Distribution Comparison")
    plt.legend()
    plt.tight_layout()
    out_path = os.path.join(plots_dir, f"{col}_distributions_{period1_start}_{period1_end}_vs_{period2_start}_{period2_end}.png")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(gausspath, f"{col}_gaussian_comparison from {period1_start} to {period1_end} and {period2_start} to {period2_end}.png"))
    plt.close() 

def plotpermonth(df, col, frequency):
    if frequency == 'Y':
            resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        pass
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")

    for i in range(1, 13):
        target_month = i
        monthly_data = resampled[resampled.index.month == target_month]
        data_to_plot = monthly_data[col]
        plt.figure(figsize=(12, 6))
        plt.plot(data_to_plot.index, data_to_plot.values, marker='o', linestyle='-', alpha=0.7)
        plt.title(f'{col} for month  {target_month} ')
        plt.xlabel("Year")
        unit = unitdict.get(col)
        if unit is not None: 
            plt.ylabel(f"{col} ({unit})")
        else: 
            plt.ylabel(f"{col}")

        plt.grid(True)
        plt.tight_layout()
        out_path = os.path.join(permonthpath, f"{col} for month {i} _{frequency} .png")
        plt.savefig(out_path)
        plt.close()
def plotclimatological(df,col):
    groupby_month = df.groupby(df.index.month).agg(aggdict)
    plt.figure(figsize=(12, 6))
    plt.plot(groupby_month.index, groupby_month[col], marker='', linestyle='-', alpha=0.7)
    plt.title(f'Climatological {col} ( by Month)')
    plt.xticks(range(1, 13))
    month_letters = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    plt.gca().set_xticklabels(month_letters)
    plt.xlabel("Month")
    unit = unitdict.get(col)
    if unit is not None: 
        plt.ylabel(f"{col} ({unit})")
    else: 
        plt.ylabel(f"{col}")

    plt.grid(True)
    plt.tight_layout()
    
    out_path = os.path.join(climatologicalpath, f"Climatological {col}.png")
    plt.savefig(out_path)


def plotseasonal(df, usecols, frequency= False, fit=False):
    
    resampled = df.resample('QE-FEB').agg(aggdict)    
    upperend=len(resampled)-4
    print("Note: For seasonal data plots, the frequency is auto-set to Quarterly ")
    
    winterdf = resampled.iloc[4:upperend:4].copy()
    springdf = resampled.iloc[1::4]
    summerdf = resampled.iloc[2::4]
    autumndf = resampled.iloc[3::4]
    seasons = [('Spring', springdf), ('Summer', summerdf), ('Autumn', autumndf), ('Winter', winterdf)]

    for col in usecols:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)

        for (name, s_df), ax in zip(seasons, axes.flat):
            ax.plot(s_df.index, s_df[col])
            if fit:
                X = sm.add_constant(s_df.index.to_julian_date().values)
                Y = s_df[col].values
                model = sm.OLS(Y, X)
                results = model.fit()
                intercept = results.params[0]
                slope = results.params[1]*365
                equation = f'Linear Fit (Slope: {slope:.5f})'
                ax.plot(s_df.index, results.predict(X), color='red', label=equation)
            ax.legend()
            ax.set_title(f"{col} - {name}")
            unit = unitdict.get(col)
            ax.set_ylabel(f"{col} ({unit})")
            ax.grid(True)
            
        fig.supxlabel("UTC")
        plt.tight_layout()
        os.makedirs(os.path.join(plots_dir,"per season"), exist_ok=True)
        out_path = os.path.join(plots_dir,"per season", f"{col}_Q_grid.png")
        plt.savefig(out_path)
        plt.close()

def plotpermonthbarchart(df, usecols):
    print(df.index)
    print(type(df.index))
    for col in usecols:
        
        resampled= df.groupby(df.index.month).agg(aggdict)
        month_names = list(calendar.month_abbr)[1:]
        plt.figure(figsize=(12, 6))
        plt.bar(month_names, resampled[col].values, color='skyblue', edgecolor='black')
        plt.title(f'{col} - month ')
        plt.xlabel("Month")
        unit = unitdict.get(col)
        if unit is not None: 
            plt.ylabel(f"{col} ({unit})")
        else: 
            plt.ylabel(f"{col}")

        plt.grid(True)
        plt.tight_layout()
        out_path = os.path.join(plots_dir, f"{col} seasonal .png")
        plt.savefig(out_path)
        plt.close()

        
'''-----PLOTTING TREND-----'''

def plottrend(df, col, frequency):
    if frequency == 'Y':
            resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")

    X = resampled.index.to_julian_date().values
    Y = resampled[col].values
    

    mask = ~np.isnan(Y) 
    X_masked = X[mask]
    Y_masked = Y[mask]  
    index_masked = resampled.index[mask]
    X = sm.add_constant(X_masked)
    model = sm.OLS(Y_masked, X, missing='drop')
    results = model.fit()
    intercept = results.params[0]
    slope = results.params[1]*365
    equation = f'Linear Fit (Slope: {slope:.5f})'

    t_res = results.t_test([1, 0])
    t_res_list = t_res.summary_frame().values.tolist()[0]
    t_res_frame = t_res.summary_frame()
    t_res_frame.insert(0, 'column', col)  
    plt.figure(figsize=(10, 6))
    plt.plot(resampled.index, resampled[col], label='Data')
    plt.plot(index_masked, results.fittedvalues, color='red', label=equation)
    plt.xlabel("UTC")
    unit = unitdict.get(col)
    if unit is not None: 
        plt.ylabel(f"{col} ({unit})")
    else: 
        plt.ylabel(f"{col}")
    plt.title(f"{col} Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    out_path = os.path.join(trendspath, f"{col}_trends_{frequency}.png")
    plt.savefig(out_path)
    plt.close()
    return t_res_frame
    

def plotsharedtemp(df, usecols, frequency):
    if frequency == 'Y':
        resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    elif frequency == 'Q':
        resampled = df.resample('QE-FEB').agg(aggdict)
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")
       
    plt.figure(figsize=(10, 6))
    plt.plot(resampled.index, resampled['TairMax'], label='TairMax', color='red')
    plt.plot(resampled.index, resampled['TairAv'], label='TairAv', color='blue')
    plt.plot(resampled.index, resampled['TairMin'], label='TairMin', color='green')
    plt.xlabel("UTC")
    plt.ylabel("Temperature (C)")

    valid_range = resampled.dropna(subset=['TairMax', 'TairMin']).index
    plt.xlim(valid_range.min(), valid_range.max())
    plt.title("Temperature Over Time")
    plt.grid(True)
    plt.tight_layout()
    out_path = os.path.join(plots_dir, f"Temperature_{frequency}.png")
    plt.savefig(out_path)
    plt.close()

def plot2climatologicals(df,col,starttime1, endtime1, starttime2, endtime2):
    df1 = df[(df.index >= starttime1) & (df.index <= endtime1)]
    df2 = df[(df.index >= starttime2) & (df.index <= endtime2)]
    df1 = df1.resample('ME').agg(aggdict)
    df2 = df2.resample('ME').agg(aggdict)
    
    groupby_month1 = df1.groupby(df1.index.month).mean()
    groupby_month2 = df2.groupby(df2.index.month).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(groupby_month1.index, groupby_month1[col], marker='', linestyle='-', alpha=0.7, label=f'Period 1: {starttime1.year} to {endtime1.year}')
    plt.plot(groupby_month2.index, groupby_month2[col], marker='', linestyle='-', alpha=0.7, label=f'Period 2: {starttime2.year} to {endtime2.year}')
    plt.title(f'Climatological {col} ( by Month)')
    plt.xticks(range(1, 13))
    month_letters = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    plt.gca().set_xticklabels(month_letters)
    plt.xlabel("Month")
    unit = unitdict.get(col)
    if unit is not None: 
        plt.ylabel(f"{col} ({unit})")
    else: 
        plt.ylabel(f"{col}")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    out_path = os.path.join(climatologicalpath, f"Shared Climatological {col}.png")
    plt.savefig(out_path)
def plotcomparativeclimatological(df,col,date1, date2, date3, date4):
    date_ranges = [(date1, date2), (date3, date4)]
    df1 = df[(df.index >= date1) & (df.index <= date2)]
    df2 = df[(df.index >= date3) & (df.index <= date4)]
    for df in [df1, df2]:
            
        groupby_month = df.groupby(df.index.month).agg(aggdict)
        plt.figure(figsize=(12, 6))
        plt.plot(groupby_month.index, groupby_month[col], marker='', linestyle='-', alpha=0.7)
        plt.title(f'Climatological {col} ( by Month)')
        plt.xticks(range(1, 13))
        month_letters = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        plt.gca().set_xticklabels(month_letters)
        plt.xlabel("Month")
        unit = unitdict.get(col)
        if unit is not None: 
            plt.ylabel(f"{col} ({unit})")
        else: 
            plt.ylabel(f"{col}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.close()



def plot2trends(df, col, date1, date2, date3, date4, frequency):
    if frequency == 'Y':
        resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")
    
    date_ranges = [(date1, date2), (date3, date4)]
    df1 = resampled[(resampled.index >= date1) & (resampled.index <= date2)]
    df2 = resampled[(resampled.index >= date3) & (resampled.index <= date4)]
    plt.figure(figsize=(10, 6))
    plt.plot(resampled.index, resampled[col], label='Data')
    for df, color in zip([df1, df2], ['red', 'blue']):
    
        X = df.index.to_julian_date().values
        Y = df[col].values
        mask = ~np.isnan(Y) 
        X_masked = X[mask]
        Y_masked = Y[mask]  
        index_masked = df.index[mask]
        X = sm.add_constant(X_masked)
        model = sm.OLS(Y_masked, X, missing='drop')
        results = model.fit()
        slope = results.params[1]*365
        equation = f'Linear Fit (Slope: {slope:.5f})'
        plt.plot(index_masked, results.fittedvalues, color=color, label=equation)
    plt.xlabel("UTC")
    unit = unitdict.get(col)
    if unit is not None: 
        plt.ylabel(f"{col} ({unit})")
    else: 
        plt.ylabel(f"{col}")
    plt.title(f"{col} Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    out_path = os.path.join(trendspath, f"{col}_double_trends_{frequency}.png")
    plt.savefig(out_path)
    plt.close()

def plotanomalytrend(df, col, frequency):
    if frequency == 'Y':
            resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")

    resampled[col] = resampled[col] - resampled[col].mean()

    X = resampled.index.to_julian_date().values
    Y = resampled[col].values
  
    mask = ~np.isnan(Y) 
    X_masked = X[mask]
    Y_masked = Y[mask]  
    index_masked = resampled.index[mask]
    X = sm.add_constant(X_masked)
    model = sm.OLS(Y_masked, X, missing='drop')
    results = model.fit()
    intercept = results.params[0]
    slope = results.params[1]*365
    equation = f'Linear Fit (Slope: {slope:.5f})'

    t_res = results.t_test([0, 1])
    
    t_res_list = t_res.summary_frame().values.tolist()[0]
    t_res_frame = t_res.summary_frame()
    t_res_frame.insert(0, 'column', col)  
    plt.figure(figsize=(10, 6))
    plt.plot(resampled.index, resampled[col], label='Data')
    plt.plot(index_masked, results.fittedvalues, color='red', label=equation)
    plt.xlabel("UTC")
    unit = unitdict.get(col)
    plt.ylabel(f"{col} anomaly ({unit})")
    plt.title(f"{col} anomalies Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    out_path = os.path.join(trendspath, f"{col}_trends_anomaly {frequency}.png")
    plt.savefig(out_path)
    plt.close()
    return t_res_frame


def plot2anomalytrends(df, col, date1, date2, date3, date4, frequency):
    if frequency == 'Y':
        resampled = df.resample('YE').agg(aggdict)
    elif frequency == 'M':
        resampled = df.resample('ME').agg(aggdict)
    elif frequency == 'D':
        resampled = df.resample('D').agg(aggdict)
    elif frequency == 'H':
        resampled = df.copy()
    else:
        print("Invalid frequency. Choose 'yearly', 'monthly', or 'daily'.")

    resampled[col] = resampled[col] - resampled[col].mean()
    df1 = resampled[(resampled.index >= date1) & (resampled.index <= date2)]
    df2 = resampled[(resampled.index >= date3) & (resampled.index <= date4)]
    plt.figure(figsize=(10, 6))
    plt.plot(resampled.index, resampled[col], label='Data')
    for df in [df1, df2]:
    
        X = df.index.to_julian_date().values
        Y = df[col].values
        mask = ~np.isnan(Y) 
        X_masked = X[mask]
        Y_masked = Y[mask]  
        index_masked = df.index[mask]
        X = sm.add_constant(X_masked)
        model = sm.OLS(Y_masked, X, missing='drop')
        results = model.fit()
        slope = results.params[1]*365
        equation = f'Linear Fit (Slope: {slope:.5f})'
        plt.plot(index_masked, results.fittedvalues, color='red', label=equation)
    plt.xlabel("UTC")
    unit = unitdict.get(col)
    plt.ylabel(f"{col} anomaly ({unit})")
    plt.title(f"{col} anomaly Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    out_path = os.path.join(trendspath, f"{col}_double_anomaly_trends_{frequency}.png")
    plt.savefig(out_path)
    plt.close()

def plotseasonalanomaly(df, usecols, frequency= False, fit=False):
    
    resampled = df.resample('QE-FEB').agg(aggdict)   
    resampled
    upperend=len(resampled)-4
    print("Note: For seasonal data plots, the frequency is auto-set to Quarterly ")
    
    winterdf = resampled.iloc[4:upperend:4].copy()
    springdf = resampled.iloc[1::4]
    summerdf = resampled.iloc[2::4]
    autumndf = resampled.iloc[3::4]
    seasons = [('Spring', springdf), ('Summer', summerdf), ('Autumn', autumndf), ('Winter', winterdf)]

    for (name,df) in seasons:
        df[usecols] = df[usecols] - df[usecols].mean()

    for col in usecols:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)

        for (name, s_df), ax in zip(seasons, axes.flat):
            ax.plot(s_df.index, s_df[col])
            if fit:
                X = sm.add_constant(s_df.index.to_julian_date().values)
                Y = s_df[col].values
                model = sm.OLS(Y, X)
                results = model.fit()
                intercept = results.params[0]
                slope = results.params[1]*365
                equation = f'Linear Fit (Slope: {slope:.5f})'
                ax.plot(s_df.index, results.predict(X), color='red', label=equation)
            ax.legend()
            ax.set_title(f"{col} - {name} anomaly")
            unit = unitdict.get(col)
            ax.set_ylabel(f"{col} ({unit}) anomaly")
            ax.grid(True)
            
        fig.supxlabel("UTC")
        plt.tight_layout()
        os.makedirs(os.path.join(plots_dir,"per season"), exist_ok=True)
        out_path = os.path.join(plots_dir,"per season", f"{col}_Q_grid anomalies.png")
        plt.savefig(out_path)
        plt.close()

def plot_gaussians_by_location(df, usecols, plots_dir):
    for col in usecols:
        unstacked = df[col].unstack(level="Location")
        global_min = unstacked.min().min()
        global_max = unstacked.max().max()
        x = np.linspace(global_min - 5, global_max + 5, 200)
        plt.figure(figsize=(10, 6))

        for location in unstacked.columns:
            series = unstacked[location].dropna()
            mean, std = series.mean(), series.std()
            pdf = stats.norm.pdf(x, mean, std)
            plt.plot(
                x,
                pdf,
                linewidth=2,
                label=f"{location}: $\\mu={mean:.1f}, \\sigma={std:.1f}$",
            )
            plt.fill_between(x, pdf, alpha=0.1)
        label = "Mean Temperature" if col == "TairAv" else col
        plt.xlabel(f"{label} ")
        plt.ylabel("Probability Density")
        plt.title(f"{label} Distribution by Location")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        os.makedirs(os.path.join(plots_dir, "gaussian_plots"), exist_ok=True)
        out_path = os.path.join(plots_dir, "gaussian_plots", f"{col}_gaussian_locations.png")
        plt.savefig(out_path)
        plt.close()

def plotcolsbylocation(df, usecols):
        
    for col in usecols:
        df[col].unstack(level='Location').plot(figsize=(10, 6))
        plt.title(f'{col} Comparison')
        unit = unitdict.get(col)
        plt.ylabel(f"{col} ({unit})")
        plt.grid(True)
        plt.savefig(f'{col}_comparison.png')
        plt.savefig(os.path.join(plots_dir, f"{col}_locations.png"))
        plt.close()