import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#Accessing The Data
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")


#Seperating Date and Time from Timestamp format

df['Dates'] = pd.to_datetime(df['datetime']).dt.date
df['Time'] = pd.to_datetime(df['datetime']).dt.time
df = df.drop(columns="datetime")

#Pivot Tables for each Region
west_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="West", aggfunc="mean", margins="True")
east_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="East", aggfunc="mean", margins="True")
north_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="North", aggfunc="mean", margins="True")
south_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="South", aggfunc="mean", margins="True")
national_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="National", aggfunc="mean", margins="True")
northeast_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="North East", aggfunc="mean", margins="True")


#Plotting
hours = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
plt.plot(hours, west_pivoted.loc["All"][0:-1])
plt.xlabel("Hour of the Day (24 Hour Format)")
plt.ylabel("Average load over 5 yr interval")
plt.xticks(hours)
plt.show()



