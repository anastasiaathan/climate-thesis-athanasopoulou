from plotting import (plot1gaussian, plot2climatologicals, plotcols
                      , plot2gaussians, plottrend, plotpermonth,
                        plotclimatological, plotseasonal, plotpermonthbarchart, 
                        plotsharedtemp, plot2trends, plot2anomalytrends,
                        plotanomalytrend, plotseasonalanomaly, 
                        plot_gaussians_by_location, plotcolsbylocation)
from config import *
import pandas as pd

"-----Preprocessing-----"
# """
if preprocessing == True:
    print("Preprocessing for station ", station)
    if station == "mitilini":
        from preprocessMitilini import *
    elif station == "sigri":
        from preprocessSigri import *
    elif station == "combined":
        from preprocessCombined import *
    # """
"""-----Plotting-----"""
# At first, we need to prepare the data for plotting

if plotting == True:
    df= pd.read_csv(os.path.join(dataframes_dir, station, f"filtered_{station}.csv"))
    df['UTC'] = pd.to_datetime(df['UTC'], format='ISO8601')
    df.set_index('UTC', inplace= True)
    df.sort_index(inplace=True)   
    df = df[df.index.year < df.index.year.max()] 
    df.drop_duplicates(inplace=True)

    qcols= [col for col in df.columns if 'QC' in col]
    colstodrop= (["UTC", "Frequency", "StnCode", 
                "Year", "Day", "Hour/Min", 
                "BatteryVolt", "WD", "TsoilAv", 
                "TsoilMax", "TsoilMin", "RHFuelAv", 
                "RHFuelMax", "RHFuelMin", "TempFuelAv",
                "TempFuelMax", "TempFuelMin", "RainDur60" ])

    colstoplot = [col for col in df.columns if col not in qcols + colstodrop]

    if station == "combined":
        print ("Plotting for both stations" )
    else:
        print("Plotting for station ", station)


    # ----------------MITILINI----------------


    if station == "mitilini":

        # ---------double trend for Temperature---------
        starttime1,endtime1 = [pd.to_datetime('1955-01-01'), pd.to_datetime('1985-12-31')]
        starttime2,endtime2 = [pd.to_datetime('1995-01-01'), df.index.max()]
        plot2trends(df, 'TairAv',starttime1,endtime1,starttime2,endtime2, frequency="Y")

        # ---------trend for rest of the plots--------- 
        frequency= 'Y'
        t_res_list = []
        for col in colstoplot:
            t_res_frame = plottrend(df, col, frequency='Y')
            t_res_list.append(( t_res_frame))
        t_res_df = pd.concat(t_res_list, ignore_index=True)
        t_res_df.to_csv(trendspath + f't_test_results_{frequency}.csv', index=False)

        # ----------Seasonal ----------
        plotseasonal(df, colstoplot, frequency)

        # ----------Data plotting----------
        plotcols(df, colstoplot, frequency)

        # ----------Gaussian plots ----------
        starttime=df.index.min()
        endtime=df.index.max()
        plot1gaussian(df,'TairAv', starttime, endtime)
        # ----------Double Climatological plots ----------

            # 1.Rain 
        starttime1,endtime1 = [pd.to_datetime('1975-01-01'), pd.to_datetime('2000-12-31')]
        starttime2,endtime2 = [pd.to_datetime('2001-01-01'), df.index.max()]
        plot2climatologicals(df,'Rain',starttime1,endtime1,starttime2,endtime2)

            # 2. Temperature 
        starttime1,endtime1 = [pd.to_datetime('1955-01-01'), pd.to_datetime('1985-12-31')]
        starttime2,endtime2 = [pd.to_datetime('1995-01-01'), df.index.max()]
        plot2climatologicals(df,'TairAv',starttime1,endtime1,starttime2,endtime2)



    # -----------------SIGRI----------------
    if station == "sigri":
        frequency= 'M'
        # monthly anomaly trend
        t_res_list = []
        for col in colstoplot:
            t_res_frame = plotanomalytrend(df, col, frequency="M")
            t_res_list.append(( t_res_frame))
        t_res_df = pd.concat(t_res_list, ignore_index=True)
        t_res_df.to_csv(trendspath + f't_test_results_anomalies.csv', index=False)
        # ----------Seasonal ----------  
        plotseasonalanomaly(df,colstoplot, frequency, fit= False)

        # ----------Gaussian plots ----------
        starttime=df.index.min()
        endtime=df.index.max()
        plot1gaussian(df,'TairAv', starttime, endtime)



    # -----------------COMBINED----------------
    if station == "combined":
        frequency= 'M'
        df.set_index('Location', append=True, inplace=True)
        df.sort_index(inplace=True)
        combinedcolstoplot= ['TairAv', 'WS (knots)', 'Rain']
        plot_gaussians_by_location(df, ['TairAv'], plots_dir)
        plotcolsbylocation(df, combinedcolstoplot)



