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


#Pivot Tables for each Region
region = "National" # East, West, North, South, National, North East
start_date = (2019, 1, 1) #(year, month, day)
end_date = (2024, 4, 30)
pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values=region)

#DataFrame not Pivot Table
df_region_interval = pivoted_region.loc[datetime.date(*start_date):datetime.date(*end_date)] 
avg_day_in_region_in_interval = df_region_interval.aggregate("mean", axis=0)



#---------PLOTTING---------------
ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
plt.plot(ticks, avg_day_in_region_in_interval)
plt.xticks(ticks)
plt.show()
