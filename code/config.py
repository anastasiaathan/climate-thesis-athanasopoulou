station= "combined"
preprocessing = True
plotting = False
import os 
cwd= os.getcwd()
inputpath=os.path.join(cwd,'input')
os.makedirs(inputpath, exist_ok=True)
dataframes_dir = os.path.join(cwd, "dataframes")
os.makedirs(dataframes_dir, exist_ok=True)

plots_dir = os.path.join(cwd, "plots", station)
os.makedirs(plots_dir, exist_ok=True)




mitiliniinput=os.path.join(cwd, "input", "mitilini")
sigriinput=os.path.join(cwd, "input", "sigri")


"""------------MITILINI------------"""

mitilini_path_1 = os.path.join(mitiliniinput, "Mytilini12hrPrecip1.1.1955-28.2.2021.xlsx")
mitilini_path_2 = os.path.join(mitiliniinput, "MytiliniOpenEMY.csv")
mitilini_path_3 = os.path.join(mitiliniinput, "MytiliniClosedEMY.csv")
mitilini_path_4 = os.path.join(mitiliniinput, "ΜΥΤΙΛΗΝΗ ΥΕΤΟΣ 12ΩΡΟΥ 2021_2025.xlsx")
mitilini_path_5 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Θερμοκρασία_Άνεμος_Σχ.Υγρασία_2021_3.2025.xls")
mitilini_path_6 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Νέφωση_1955_1959.xls")
mitilini_path_7 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Νέφωση_1960_1964.xls")
mitilini_path_8 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Νέφωση_1965_1969.xls")
mitilini_path_9 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Νέφωση_1970_1974.xls")
mitilini_path_10 = os.path.join(mitiliniinput, "2025.1685_Μυτιλήνη_3ωρες_Τιμές_Νέφωση_2021_3.2025.xls")

"""------------SIGRI------------"""

file1path=os.path.join(sigriinput,'Sigri_old.dat')#2015-2020
file2path=os.path.join(sigriinput,'Sigri.dat') #2019-2021
file3path=os.path.join(sigriinput,'Sigri_final_storage_1.dat') #2021-2024 exei problem
file4path=os.path.join(sigriinput,'Sigri_final_storage_new.dat')#2024-2025


sigriheader110=['Frequency','StnCode','Year','Day','Hour/Min','TairAv','TairMax','TairMin','RHAv','RHMax','RHMin','WS(m per s)','WD','WSmax','Precipitation','PrecipDuration10(min)','PatmAv','PatmMax','PatmMin','TempFuelAv','TempFuelMax','TempFuelMin','RHFuelAv','RHFuelMax','RHFuelMin','TsoilAv','TsoilMax','TsoilMin','SRAdirAv','IRRadAv']
sigriheader160=['Frequency','StnCode','Year','Day','Hour/Min','Rain','RainDur60','TempFuelAv','TempFuelMax','TempFuelMin','RHFuelAv','RHFuelMax','RHFuelMin','TsoilAv','TsoilMax','TsoilMin','BatteryVolt','TairAv','RHAv','WS(m per s)','WD','PatmAv','TairMax','TairMin','RHMax','RHMin','WSmax','PatmMax','PatmMin','SolRadAv','IRRadAv']

df110path, df160path = os.path.join(dataframes_dir, 'sigri', 'df110.csv'), os.path.join(dataframes_dir, 'sigri', 'df160.csv')



gausspath=os.path.join(plots_dir,'gaussian_plots')
trendspath=os.path.join(plots_dir,'trend_plots')
permonthpath=os.path.join(plots_dir,'permonth')
climatologicalpath=os.path.join(plots_dir,'climatological')
for path in [gausspath, trendspath, permonthpath, climatologicalpath]:
    os.makedirs(path, exist_ok=True)

combineddir = os.path.join(dataframes_dir, "combined")
os.makedirs(combineddir, exist_ok = True)

rename_map1 = {
        "ΕΤΟΣ": "Year",
        "ΜΗΝΑΣ": "Month",
        "ΗΜΕΡΑ": "Day",
        "ΩΡΑ UTC": "Hour",
        "ΤΙΜΗ": "Rain"
    }

rename_map2 = {
    "YEAR": "Year",
    "MONTH": "Month",
    "DAY": "Day",
    "UTC": "Hour",
    "BARPRESSURE": "PatmAv",
    "DRYTEMP": "TairAv",
    "WETTEMP": "wetTemperature",
    "MAXTEMP": "TairMax",
    "MINTEMP": "TairMin",
    "RELHUMIDITY": "RHAv",
    "WINDDIRECTION": "WD",
    "WINDFORCEKNOT": "WS (knots)",
    "VISIBILITY": "visibility",
    "TOTALCLOUDAMOUNT": "Cloudiness",
    "PRECIPHEIGHT": "Rain"
}
rename_map3 = {
    "YEAR": "Year",
    "MONTH": "Month",
    "DAY": "Day",
    "UTC": "Hour",
    "Wind_Direction": "WD",
    "WINDFORCEKNOT": "WS (knots)",
    "Max_Wind_Force_Knot": "WSmax",
    "DRYTEMP": "TairAv",
    "Dew_Point": "dewPoint",
    "RELHUMIDITY": "RHAv",
}
rename_map4 = {
    "ΕΤΟΣ": "Year",
    "ΜΗΝΑΣ": "Month",
    "ΗΜΕΡΑ": "Day",
    "ΩΡΑ UTC_hour": "Hour",
    "ΥΨΟΣ ΥΕΤΟΥ": "Rain",
}
rename_map5 = {
    "Έτος": "Year",
    "Μήνας": "Month",
    "Ημέρα": "Day",
    "Ώρα (UTC)": "Hour",
    "Διεύθυνση Ανέμου (°)": "WD",
    "Μέγιστη Ένταση Ανέμου  (knots)": "WSmax",
    "Ένταση Ανέμου (knots)": "WS (knots)",
    "Ένταση Ανέμου (Bf)": "WS (Beaufort)",
    "Θερμ/σία (°C)": "TairAv",
    "Σχετική Υγρασία  (%)": "RHAv",
}
rename_map6_10={
        "ΕΤΟΣ": "Year",
        "ΜΗΝΑΣ": "Month",
        "ΗΜΕΡΑ": "Day",
        "ΩΡΑ UTC": "Hour",
        "ΤΙΜΗ": "Cloudiness"
    }
limdictmitilini={
    "Rain": { "min": 0, "max": 1000 },
    "PatmAv": { "min": 900, "max": 1100 },
    "TairAv": { "min": -10, "max": 47 },
    "wetTemperature": { "min": -10, "max": 47 },
    "TairMax": { "min": -10, "max": 47 },
    "TairMin": { "min": -10, "max": 47 },
    "RHAv": { "min": 0, "max": 100 },
    "WD": { "min": 0, "max": 360 },
    "WS (knots)": { "min": 0, "max": 100 },
    "visibility": { "min": 0, "max": 10000 },
    "Cloudiness": { "min": 0, "max": 8 },
    "WSmax": { "min": 0, "max": 100 },
    "dewPoint": { "min": -10, "max": 47 },
    "WS (Beaufort)": { "min": 0, "max": 12 }
}

errdictmitilini = {
    "WD": "VRB",
    "Rain": "-",
    "PatmAv":  "-",
    "TairAv":  "-",
    "wetTemperature":  "-",
    "TairMax":  "-",
    "TairMin":  "-",
    "RHAv":  "-",
    "WD":  "-",
    "WS (knots)":  "-",
    "visibility": "-",
    "Cloudiness": "-",
    "WSmax": "-",
    "dewPoint": "-",
    "WS (Beaufort)": "-"
}


errdictsigri= {
    "Rain": "6999",
    "RainDur60": "6999",
    "TairAv": "6999",
    "TairMax": "6999",
    "TairMin": "6999",

    "RHAv": "6999",
    "RHMax": "6999",
    "RHMin": "6999",

    "WS(m per s)": "6999",
    "WD": "6999",
    "WSmax": "6999",

    "PatmAv": "6999",
    "PatmMax": "6999",
    "PatmMin": "6999",

    "SolRadAv": "6999",
    "IRRadAv": "6999",

    "TsoilAv": "6999",
    "TsoilMax": "6999",
    "TsoilMin": "6999",
    "TempFuelMax": "6999",
    "TempFuelMin": "6999",

    "RHFuelAv": "6999",
    "RHFuelMax": "6999",
    "RHFuelMin": "6999",

    "BatteryVolt": "6999"
}

limdictsigri = {
        # --- Precipitation & Moisture ---
        'Rain': {'min': 0.0, 'max': 50.0},        # mm (assuming hourly/daily accumulation. 300mm is extreme flood)
        'RainDur60': {'min': 0.0, 'max': 60.0},    # Minutes of rain per hour
        
        # --- Air Temperature (Celsius) ---
        'TairAv': {'min': -20.0, 'max': 55.0},     
        'TairMax': {'min': -20.0, 'max': 55.0},
        'TairMin': {'min': -20.0, 'max': 55.0},
        
        # --- Relative Humidity (%) ---
        'RHAv': {'min': 10.0, 'max': 100.0},
        'RHMax': {'min': 10.0, 'max': 100.0},
        'RHMin': {'min': 10.0, 'max': 100.0},
        
        # --- Wind (m/s and Degrees) ---
        'WS(m per s)': {'min': 1.0, 'max': 60.0},  # 60 m/s is ~215 km/h (Category 4 hurricane)
        'WSmax': {'min': 9, 'max': 70.0},        # Allowing a slightly higher cap for extreme gusts
        'WD': {'min': 0.0, 'max': 360.0},          # Degrees on a compass
        
        # --- Atmospheric Pressure (hPa / mbar) ---
        # Sigri is at sea level, so pressure rarely drops below 960 or above 1040.
        'PatmAv': {'min': 950.0, 'max': 1050.0},   
        'PatmMax': {'min': 950.0, 'max': 1050.0},
        'PatmMin': {'min': 950.0, 'max': 1050.0},
        
        # --- Radiation (W/m^2) ---
        'SolRadAv': {'min': 0.0, 'max': 1400.0},   # Cannot exceed the solar constant (~1361 W/m^2)
        'IRRadAv': {'min': 100.0, 'max': 700.0},   # Longwave/Infrared limits for typical Earth surfaces
        
        # --- Soil & Fuel Temperatures (Celsius) ---
        # Surfaces get hotter than air in direct sunlight and hold heat differently.
        'TsoilAv': {'min': -15.0, 'max': 65.0},
        'TsoilMax': {'min': -15.0, 'max': 65.0},
        'TsoilMin': {'min': -15.0, 'max': 65.0},
        'TempFuelAv': {'min': -20.0, 'max': 75.0}, # Dark fuel in direct summer sun gets very hot
        'TempFuelMax': {'min': -20.0, 'max': 75.0},
        'TempFuelMin': {'min': -20.0, 'max': 75.0},
        
        # --- Fuel Humidity (%) ---
        'RHFuelAv': {'min': 0.0, 'max': 100.0},
        'RHFuelMax': {'min': 0.0, 'max': 100.0},
        'RHFuelMin': {'min': 0.0, 'max': 100.0},
        
        # --- System / Hardware ---
        # Assuming a standard 12V weather station system.
        'BatteryVolt': {'min': 9.0, 'max': 15.0}  
         
    }


def sum_vals(x):
    return x.sum(min_count=1)

aggdictmitilini = {
    "PatmAv": 'mean',
    "TairAv": 'mean',
    "wetTemperature": 'mean',
    "RHAv": 'mean',
    "WD": 'mean',
    "WS (knots)": 'mean',
    "visibility": 'mean',
    "Cloudiness": 'mean',
    "dewPoint": 'mean',
    "WS (Beaufort)": 'mean',
    "TairMax": 'mean',
    "TairMin": 'mean',

    "WSmax": 'mean',
    "Rain": sum_vals,
}


aggdictsigri110 = {
'TairAv': 'mean',
'RHAv': 'mean',
'WS(m per s)': 'mean',
'WD': 'mean',
'PatmAv': 'mean',
'SRAdirAv': 'mean',
'IRRadAv': 'mean',
'TairMax': 'mean',
'TairMin': 'mean',

'RHMax': 'mean',
'WSmax': 'mean',
'PatmMax': 'mean',

'RHMin': 'mean',
'PatmMin': 'mean',

'Precipitation': sum_vals,
'PrecipDuration10(min)': sum_vals
}

aggdictsigri160 = {
    # Sums (Rain/Duration)
    'Rain': sum_vals,
    'RainDur60': sum_vals,
    
    # Averages
    'TempFuelAv': 'mean',
    'RHFuelAv': 'mean',
    'TsoilAv': 'mean',
    'BatteryVolt': 'mean',
    'TairAv': 'mean',
    'RHAv': 'mean',
    'WS(m per s)': 'mean',
    'WD': 'mean',
    'PatmAv': 'mean',
    'SolRadAv': 'mean',
    'IRRadAv': 'mean',
    
    # Maximums
    'TempFuelMax': 'mean',
    'RHFuelMax': 'mean',
    'TsoilMax': 'mean',
    'TairMax': 'mean',
    'RHMax': 'mean',
    'WSmax': 'mean',
    'PatmMax': 'mean',
    
    # Minimums
    'TempFuelMin': 'mean',
    'RHFuelMin': 'mean',
    'TsoilMin': 'mean',
    'TairMin': 'mean',
    'RHMin': 'mean',
    'PatmMin': 'mean'
}


if station == "mitilini":
    aggdict = aggdictmitilini
elif station == "sigri":
    aggdict = aggdictsigri160
unitdict = {
    # --- Temperature ---
    "TairAv": "°C",
    "TairMax": "°C",
    "TairMin": "°C",
    "wetTemperature": "°C",
    "dewPoint": "°C",
    "TsoilAv": "°C",
    "TsoilMax": "°C",
    "TsoilMin": "°C",
    "TempFuelAv": "°C",
    "TempFuelMax": "°C",
    "TempFuelMin": "°C",
    # --- Relative Humidity ---
    "RHAv": "%",
    "RHMax": "%",
    "RHMin": "%",
    "RHFuelAv": "%",
    "RHFuelMax": "%",
    "RHFuelMin": "%",
    # --- Wind Speed & Direction ---
    "WS(m per s)": None,
    "WS (knots)": None, 
    "WS (Beaufort)":  None,
    "WSmax": "m/s", 
    "WD": "°",
    # --- Atmospheric Pressure ---
    "PatmAv": "hPa",
    "PatmMax": "hPa",
    "PatmMin": "hPa",
    # --- Solar & Radiation ---
    "SolRadAv": "W/m²",
    "SRAdirAv": "W/m²",
    "IRRadAv": "W/m²",
    # --- Precipitation & Duration ---
    "Rain": "mm",
    "Precipitation": "mm",
    "RainDur60": "min",
    "PrecipDuration10(min)": "min",
    # --- Sky & Atmospheric Conditions ---
    "visibility": "km",  
    "Cloudiness": "octas",  
    # --- Station Technical Metrics ---
    "BatteryVolt": "V",
}

# !! ONLY FOR COMBINED DF PLOTTING 
aggdict160combined = {
    # Sums (Rain/Duration)
    'Rain': sum_vals,
    'RainDur60': sum_vals,
    
    # Averages
    'TempFuelAv': 'mean',
    'RHFuelAv': 'mean',
    'TsoilAv': 'mean',
    'BatteryVolt': 'mean',
    'TairAv': 'mean',
    'RHAv': 'mean',
    'WS(m per s)': 'mean',
    'WS (knots)': 'mean',
    'WD': 'mean',
    'PatmAv': 'mean',
    'SolRadAv': 'mean',
    'IRRadAv': 'mean',
    
    # Maximums
    'TempFuelMax': 'max',
    'RHFuelMax': 'max',
    'TsoilMax': 'max',
    'TairMax': 'max',
    'RHMax': 'max',
    'WSmax': 'max',
    'PatmMax': 'max',
    
    # Minimums
    'TempFuelMin': 'min',
    'RHFuelMin': 'min',
    'TsoilMin': 'min',
    'TairMin': 'min',
    'RHMin': 'min',
    'PatmMin': 'min'
}