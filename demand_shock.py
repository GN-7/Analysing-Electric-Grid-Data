import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")

df = df.set_index("datetime")
df['Dates'] = df.index.date
df['Time'] = df.index.time
df_national = df[["National"]]

def demand_shock():
    df_national_2019_pre_lockdown = df_national.loc["2019-1-1":"2019-3-15"]
    df_national_2020_pre_lockdown = df_national.loc["2020-1-1":"2020-3-15"]

    df_pre_lockdown = pd.concat([df_national_2019_pre_lockdown, df_national_2020_pre_lockdown])
    #ALIGNING BY ISO WEEK AND WEEKDAY
    df_pre_lockdown["ISO_Week"] = df_pre_lockdown.index.isocalendar().week
    df_pre_lockdown["ISO_Weekday"] = df_pre_lockdown.index.isocalendar().day
    df_pre_lockdown["Hour"] = df_pre_lockdown.index.hour
    df_pre_lockdown["Year"] = df_pre_lockdown.index.year
    side = df_pre_lockdown.pivot_table(index=["ISO_Week", "ISO_Weekday", "Hour"], columns="Year", values="National")
    paired = side.dropna()

    growth_factor = paired[2020].mean() / paired[2019].mean() # ~1.02944

    pivoted_national = pd.pivot_table(df, index=["Dates"], columns="Time", values="National")

    df_national_2019 = pivoted_national.loc[datetime.date(2019, 1, 1):datetime.date(2019, 12, 31)] 
    day_means_2019 = df_national_2019.aggregate("mean", axis=1)
    df_national_2020 = pivoted_national.loc[datetime.date(2020, 1, 1):datetime.date(2020, 12, 31)] 
    day_means_2020 = df_national_2020.aggregate("mean", axis=1)
    day_means_2020.drop(day_means_2020.index[59], inplace=True)

    day_means_expected = day_means_2019* growth_factor
    plt.plot(range(365), day_means_2019.rolling(7).mean())
    plt.plot(range(365), day_means_2020.rolling(7).mean())
    plt.plot(range(365), day_means_expected.rolling(7).mean(), linestyle="dashed")
    plt.show()

if __name__ == "__main__":
    demand_shock()
