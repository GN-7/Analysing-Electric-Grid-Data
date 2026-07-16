import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")


#-----------------SEPERATING DATE AND TIME FROM TIMESTAMP FOR EFFECTIVE SORTING-----------------------

df['Dates'] = pd.to_datetime(df['datetime']).dt.date
df['Time'] = pd.to_datetime(df['datetime']).dt.time

#----------INITIALIZATION OF LISTS-------------


#------------MAIN LOOP FOR AVERAGES GRAPHS---------------------
def normalized_day_curves(region_list: list, year_list: list):

    plots_list = []
    if not isinstance(region_list, list):
        raise TypeError
    if not isinstance(year_list, list):
        raise TypeError
    for region, year in zip(region_list, year_list):

        if year == 2024:
            print("WARNING! DATA FOR 2024 AVAILABLE ONLY FROM 1-1-24 TO 30-4-2024")

        if year in [2019, 2020, 2021, 2022, 2023, 2024] and region in ["National", "North", "East", "West", "South", "North East"]:
            #----------------------CORE LOGIC------------------------
            pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values=region)

            #DataFrame not Pivot Table
            df_region_interval = pivoted_region.loc[datetime.date(year, 1, 1):datetime.date(year, 12, 31)]
            mean_of_day = df_region_interval.mean(axis=1)                 # 365 daily means
            normalized_days  = df_region_interval.div(mean_of_day, axis=0)     # each day ÷ its OWN mean
            normalized_day   = normalized_days.mean(axis=0)                    # then average the shapes

            assert np.allclose(normalized_days.mean(axis=1), 1.0), "normalization invariant broken"
            plots_list.append(normalized_day)
        else:
            print("Enter Data as specified!")
            return None


    #---------PLOTTING---------------
    ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
    colors = {2019: "#34558B", 2020: "#BA7517", 2021: "#1D5C4C", 2022: "#93373F", 2023: "#6E3D63"}
    #----------THE ACTUAL PLOTS------------
    #----------THE ACTUAL PLOTS------------
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')

    for year, plot in zip(year_list ,plots_list, strict=True):
        times = [plot.loc[datetime.time(15, 0, 0) : datetime.time(18, 0, 0)],
             plot.loc[datetime.time(18, 0, 0) : datetime.time(21, 0, 0)],
             plot.loc[datetime.time(8, 0, 0) : datetime.time(13, 0, 0)],
             ]
        ax.plot(ticks, plot, color=colors[year])
        ax.text(23.2, plot.iloc[-1], year, fontweight="bold", color=colors[year])
        print(f"Year: {year}, Time of Max Load: {plot.idxmax()}, Max Load: +{((plot.max()- 1)*100).round(2)}%")
        print(f"Morning Spike Time: {times[2].idxmax()}, Morning Spike load: +{((times[2].max()-1)*100).round(2)}%")
        print(f"Afternoon Dip Time: {times[0].idxmin()}, Afternoon Dip load: +{((times[0].min()-1)*100).round(2)}%")
        print(f"Decline from Morning Spike: +{(((times[2].max()-1)*100) - ((times[0].min()-1)*100)).round(2)}%")
        print(f"Evening spike time: {times[1].idxmax()}, Evening spike load: +{((times[1].max()-1)*100).round(2)}%")
        print("-"*50)
    #---------PLOT CUSTOMIZATION------------------
    plt.title("Normalized Day")
    plt.plot(ticks, [1 for i in range(24)], linestyle="dashed", color="gray")
    ax.set_title("India's Average Day, Normalized", fontweight="bold")
    ax.set_xlabel('Hour of day', fontweight="bold")
    ax.set_ylabel('Deviation from mean', fontweight="bold")
    ax.set_xlim(0, 24.6)
    ax.set_xticks(ticks)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
    plt.show()

if __name__ == "__main__":
    
    normalized_day_curves(["National", "National", "National", "National", "National"], [2019, 2020, 2021, 2022, 2023])