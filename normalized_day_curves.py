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

#----------INITIALIZATION OF LISTS-------------


#------------MAIN LOOP FOR AVERAGES GRAPHS---------------------
def normalized_day_curves(region_list: list, year_list: list):

    plots_list = []
    labels = []
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
            avg_day_in_region_in_interval = df_region_interval.aggregate("mean", axis=0) #TRY AXIS 1 ALSO FOR DIFFERENT METRIC
            mean_of_day = df_region_interval.aggregate("mean", axis=1)
            normalized_day = []
            for i, j in zip(avg_day_in_region_in_interval, mean_of_day):
                normalized_day.append(i/j)
            plots_list.append(normalized_day)

        else:
            print("Enter Data as specified!")
            return None


    #---------PLOTTING---------------
    ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)

    #----------THE ACTUAL PLOTS------------
    for plot in plots_list:
        plt.plot(ticks, plot)

    #---------PLOT CUSTOMIZATION------------------
    for rgn, yr in zip(region_list, year_list):
        labels.append(f"Region: {rgn}, Year: {yr}")    

    plt.title("Normalized Day")
    plt.plot(ticks, [1 for i in range(24)], linestyle="dashed", color="red")
    plt.xlabel("Hour of the day (24H Format)")
    plt.ylabel("Normalized Electric Load in MW")
    plt.legend(labels=labels)

    plt.show()

if __name__ == "__main__":
    
    normalized_day_curves(["National", "National", "National", "National", "National"], [2019, 2020, 2021, 2022, 2023])