import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
#Accessing The Data
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")


#Seperating Date and Time from Timestamp format

df['Dates'] = pd.to_datetime(df['datetime']).dt.date
df['Time'] = pd.to_datetime(df['datetime']).dt.time

plots_list = []
while True:
    year = int(input("Enter year: "))
    region = input("Enter Region: ")
    pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values=region)

    #DataFrame not Pivot Table
    df_region_interval = pivoted_region.loc[datetime.date(year, 1, 1):datetime.date(year, 12, 31)] 
    avg_day_in_region_in_interval = df_region_interval.aggregate("mean", axis=0)
    plots_list.append(avg_day_in_region_in_interval)
    if input("Do you want to plot?(Yes/No)").strip().lower() == "yes":
        break
    else:
        continue



#---------PLOTTING---------------
ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)

for plot in plots_list:
    plt.plot(ticks, plot)

plt.show()
