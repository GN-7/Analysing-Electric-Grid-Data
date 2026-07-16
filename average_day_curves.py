import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")


#-----------------SEPERATING DATE AND TIME FROM TIMESTAMP FOR EFFECTIVE SORTING-----------------------

df['Dates'] = pd.to_datetime(df['datetime']).dt.date
df['Time'] = pd.to_datetime(df['datetime']).dt.time

#------------MAIN LOOP FOR AVERAGES GRAPHS---------------------
def average_day_curves(region_list : list, year_list: list):
    plots_list = []
    if not isinstance(region_list, list):
        raise TypeError
    if not isinstance(year_list, list):
        raise TypeError
    
    for region, year in zip(region_list, year_list, strict=True):

        if year == 2024:
            print("WARNING! DATA FOR 2024 AVAILABLE ONLY FROM 1-1-24 TO 30-4-2024")

        if year in [2019, 2020, 2021, 2022, 2023, 2024] and region in ["National", "North", "East", "West", "South", "North East"]:
            #----------------------CORE LOGIC------------------------
            pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values=region)

            #DataFrame not Pivot Table
            df_region_interval = pivoted_region.loc[datetime.date(year, 1, 1):datetime.date(year, 12, 31)] 
            avg_day_in_region_in_interval = df_region_interval.aggregate("mean", axis=0) #TRY AXIS 1 ALSO FOR DIFFERENT METRIC
            plots_list.append(avg_day_in_region_in_interval)

        else:
            print("Enter Proper Data!")
            return None


    #---------PLOTTING---------------
    ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
    colors = {2019: "#34558B", 2020: "#BA7517", 2021: "#1D5C4C", 2022: "#93373F", 2023: "#6E3D63"}
    #----------THE ACTUAL PLOTS------------
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    for year, plot in zip(year_list ,plots_list, strict=True):
        ax.plot(ticks, plot, color=colors[year])
        ax.text(23.2, plot.iloc[-1], year, fontweight="bold", color=colors[year])
        print(f"Year: {year}, Time of Max Load: {plot.idxmax()}, Max Load: {plot.max().round(2)}")

    #---------PLOT CUSTOMIZATION------------------    

    plt.title("Average Day of given years in given regions", fontweight="bold")
    plt.xlabel('Hour of day', fontweight="bold")
    plt.ylabel('Average Demand (MW)', fontweight="bold")
    plt.xlim(0, 25.6)
    plt.xticks(ticks)
    plt.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
    plt.show()

if __name__ == "__main__":
    average_day_curves(["National", "National", "National", "National", "National"], [2019,2020, 2021, 2022, 2023])