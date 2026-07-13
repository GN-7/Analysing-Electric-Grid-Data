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
    yticks = np.linspace(0.85, 1.15, 15)
    colors = {2019: "Blue", 2020: "Orange", 2021: "Green", 2022: "Red", 2023: "Violet"}
    #----------THE ACTUAL PLOTS------------
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    for year, plot in zip(year_list ,plots_list, strict=True):
        ax.plot(ticks, plot, color=colors[year])
        ax.text(23.2, plot.iloc[-1], year, fontweight="bold", color=colors[year])

    #---------PLOT CUSTOMIZATION------------------
    plt.title("Normalized Day")
    plt.plot(ticks, [1 for i in range(24)], linestyle="dashed", color="red")
    ax.set_title("India's average day Normalized")
    ax.set_xlabel('Hour of day')
    ax.set_ylabel('Deviation from mean')
    ax.set_xlim(0, 24.6)
    ax.set_xticks([0, 6, 12, 18, 23])

    plt.show()

if __name__ == "__main__":
    
    normalized_day_curves(["National", "National", "National", "National", "National"], [2019, 2020, 2021, 2022, 2023])