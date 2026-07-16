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

def lockdown_demand_shock():
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
    day_means_2020 = day_means_2020.drop(datetime.date(2020, 2, 29))
    day_means_expected = day_means_2019* growth_factor
    print(f"Minimum Average Load of 2020: {day_means_2020.min()}, Day of Minimum Load: {day_means_2020.idxmin()}")

    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), day_means_2020.rolling(7, center=True).median())
    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), day_means_expected.rolling(7, center=True).median())
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
    plt.annotate("Lockdown 1", xy=(day_means_2020.idxmin(),day_means_2020.min()), xytext=(40,20), textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    plt.show()


def west_cyclone_demand_shock():
    west_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="West")
    west_2020 = west_pivoted.loc[datetime.date(2020, 1, 1):datetime.date(2020, 12, 31)]
    west_daily_means = west_2020.aggregate("mean", axis=1)
    y = west_daily_means
    params = {
        "textcoords":"offset points",
        "arrowprops":dict(arrowstyle="->")
    }
    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D"), y)
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"))
    plt.title("Demand Shocks In The West")
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Average Load in MW")
    plt.annotate("Lockdown 1", xy=(y.idxmin(),y.min()), xytext=(40,20),**params)
    plt.annotate("Cyclone Nisarga", xy=(y.loc[datetime.date(2020, 6, 1):datetime.date(2020, 7, 1)].idxmin(),y.loc[datetime.date(2020, 6, 1):datetime.date(2020, 7, 1)].min()), xytext=(40,-20), **params)
    plt.show()

def east_cyclone_demand_shock():
    east_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="East")
    east_2020 = east_pivoted.loc[datetime.date(2020, 1, 1):datetime.date(2020, 12, 31)]
    east_daily_means = east_2020.aggregate("mean", axis=1)
    y = east_daily_means

    params = {
        "textcoords":"offset points",
        "arrowprops":dict(arrowstyle="->")
    }
    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D"), y)
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
    plt.title("Demand Shocks In The East")
    plt.xlabel("Date")
    plt.ylabel("Average Load in MW")
    plt.annotate("Cyclone Amphan", xy=(y.idxmin(),y.min()), xytext=(40,20), **params)
    plt.show()


west_cyclone_demand_shock()
east_cyclone_demand_shock()