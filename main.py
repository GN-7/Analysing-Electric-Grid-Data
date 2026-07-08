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
year = 2020         #2019, 20, 21, 22, 23, 24
pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values=region)

df_region_year = pivoted_region.loc[datetime.date(year, 1,1):datetime.date(year, 12, 31)] #DataFrame not Pivot Table

avg_day_in_region_in_year = df_region_year.aggregate("mean", axis=0)
ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
plt.plot(ticks, avg_day_in_region_in_year)
plt.xticks(ticks, rotation="vertical")
plt.show()
