import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
#------------------MAIN FUNCTIONS------------------------------

def lockdown_demand_shock(df, arg):
    df = df.set_index("datetime")
    df['Dates'] = df.index.date
    df['Time'] = df.index.time
    df_national = df[["National"]]
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
    day_means_expected.index = pd.date_range("2020-01-01", "2020-12-31", freq="D").drop("2020-02-29")
    y = day_means_2020.rolling(7, center=True).median()

    deviation = (day_means_2020 / day_means_expected - 1) * 100
    smoothened_deviation = deviation.rolling(7, center=True).median()

    params = {
        "textcoords":"offset points",
        "arrowprops":dict(arrowstyle="->")
    }
    if arg == 0:
        min = smoothened_deviation.min()
        min_date = smoothened_deviation.idxmin()      
        duration = (smoothened_deviation.loc[datetime.date(2020, 3, 25): datetime.date(2020, 9, 1)] < -5).sum()
        print(f"Demand was below the -5% threshold on {duration} days between 25 March and 1 September. The depth was {min.round(2)}% which occured on {str(min_date)}")
        plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), deviation, color="gray", alpha=0.5, linewidth=0.7, label="Raw Deviation Percentage")
        plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), smoothened_deviation, color="#BA7517", label="Smoothened - 7 Day Median")
        plt.axhspan(-5, 5, alpha=0.5, color="lightgray", label="5% Deviation Band")
        plt.title("Deviation With Respect To Expected Value", fontweight="bold")
        plt.xlabel("Date", fontweight="bold")
        plt.ylabel("Percentage", fontweight="bold")
        plt.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
        plt.legend()
        plt.savefig(f"{base_dir}/outputs/lockdown_demand_deviation.svg")
        plt.close(None)
    elif arg == 1:
        print(f"Minimum Average Load of 2020: {day_means_2020.min()}, Day of Minimum Load: {day_means_2020.idxmin()}")
        plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), y, color="#1d5c4c", label="Smoothened Load of 2020")
        plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), day_means_2020, color="lightgrey", alpha=0.5, linewidth=0.5, label="Actual Load of 2020")
        plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D").drop(["2020-02-29"]), day_means_expected.rolling(7, center=True).median(), linestyle="dashed", color="grey", label="Expected Load of 2020")
        plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
        plt.annotate(f"Trough: -32.3%", xy=(y.idxmin(),y.min()), xytext=(40,20), **params)
        plt.title("Effect of the Lockdown on Electrical Load", fontweight="bold")
        plt.xlabel("Date", fontweight="bold")
        plt.ylabel("Average Load in MW", fontweight="bold")
        plt.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
        plt.axvspan("2020-03-25", "2020-05-31", alpha=0.12, color="grey", label="Lockdown Duration")
        plt.legend()
        plt.savefig(f"{base_dir}/outputs/lockdown_demand_shock.svg")
        plt.close(None)

    else: print("Enter 0 or 1\n0 for deviation curve\n1 for load curve")

def west_cyclone_demand_shock(df):
    df = df.set_index("datetime")
    df['Dates'] = df.index.date
    df['Time'] = df.index.time
    west_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="West")
    west_2020 = west_pivoted.loc[datetime.date(2020, 1, 1):datetime.date(2020, 12, 31)]
    west_daily_means = west_2020.aggregate("mean", axis=1)
    y = west_daily_means
    params = {
        "textcoords":"offset points",
        "arrowprops":dict(arrowstyle="->")
    }
    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D"), y, color="#d85a30")
    plt.title("Effect of Cyclone Nisarga", fontweight="bold")
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
    plt.xlabel("Date", fontweight="bold")
    plt.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
    plt.ylabel("Average Load in MW", fontweight="bold")
    plt.annotate("Lockdown 1", xy=(y.idxmin(),y.min()), xytext=(40,20),**params)
    plt.annotate("Cyclone Nisarga", xy=(y.loc[datetime.date(2020, 6, 1):datetime.date(2020, 7, 1)].idxmin(),y.loc[datetime.date(2020, 6, 1):datetime.date(2020, 7, 1)].min()), xytext=(40,-20), **params)
    plt.savefig(f"{base_dir}/outputs/west_cyclone_demand_shock.svg")
    plt.close(None)

def east_cyclone_demand_shock(df):
    df = df.set_index("datetime")
    df['Dates'] = df.index.date
    df['Time'] = df.index.time
    east_pivoted = pd.pivot_table(df, index=["Dates"], columns="Time", values="East")
    east_2020 = east_pivoted.loc[datetime.date(2020, 1, 1):datetime.date(2020, 12, 31)]
    east_daily_means = east_2020.aggregate("mean", axis=1)
    y = east_daily_means

    params = {
        "textcoords":"offset points",
        "arrowprops":dict(arrowstyle="->")
    }
    plt.plot(pd.date_range("2020-01-01", "2020-12-31", freq="D"), y, color="#93373f")
    plt.xticks(pd.date_range("2020-01-01", "2020-12-31", freq="MS"), rotation=45)
    plt.title("Effect of Cyclone Amphan", fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Average Load in MW", fontweight="bold")
    plt.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
    plt.annotate("Cyclone Amphan", xy=(y.loc[datetime.date(2020, 5, 1):datetime.date(2020, 6, 15)].idxmin(),y.loc[datetime.date(2020, 5, 1):datetime.date(2020, 6, 15)].min()), xytext=(40,-20), **params)
    plt.savefig(f"{base_dir}/outputs/east_cyclone_demand_shock.svg")
    plt.close(None)

if __name__ == "__main__":
    df = pd.read_excel(f"{base_dir}/MainData.xlsx")
    lockdown_demand_shock(df,0)
    lockdown_demand_shock(df,1)
    west_cyclone_demand_shock(df)
    east_cyclone_demand_shock(df)