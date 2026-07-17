import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np

#------------MAIN LOOP FOR AVERAGES GRAPHS---------------------
def normalized_day_curves(df):
    df['Dates'] = pd.to_datetime(df['datetime']).dt.date
    df['Time'] = pd.to_datetime(df['datetime']).dt.time
    year_list = [2019, 2020, 2021, 2022, 2023]
    plots_list = []
    if not isinstance(year_list, list):
        raise TypeError
    for year in year_list:
            #----------------------CORE LOGIC------------------------
            pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values="National")

            #DataFrame not Pivot Table
            df_region_interval = pivoted_region.loc[datetime.date(year, 1, 1):datetime.date(year, 12, 31)]
            mean_of_day = df_region_interval.mean(axis=1)                 # 365 daily means
            normalized_days  = df_region_interval.div(mean_of_day, axis=0)     # each day ÷ its OWN mean
            normalized_day   = normalized_days.mean(axis=0)                    # then average the shapes

            assert np.allclose(normalized_days.mean(axis=1), 1.0), "normalization invariant broken"
            plots_list.append(normalized_day)


    #---------PLOTTING---------------
    ticks = pd.date_range("01-01-2019", "01-02-2019", freq="h", inclusive="left").hour.astype(str)
    alphas = {2019: 0.2, 2020: 0.4, 2021:0.6, 2022: 0.8, 2023: 1}
    #----------THE ACTUAL PLOTS------------
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    output_list = []
    for year, plot in zip(year_list ,plots_list, strict=True):
        times = [plot.loc[datetime.time(15, 0, 0) : datetime.time(18, 0, 0)],
             plot.loc[datetime.time(18, 0, 0) : datetime.time(21, 0, 0)],
             plot.loc[datetime.time(8, 0, 0) : datetime.time(13, 0, 0)],
             ]
        ax.plot(ticks, (plot - 1)*100, color="#1d5c4c", label=year, alpha=alphas[year])

        print(f"Year: {year}, Time of Max Load: {plot.idxmax()}, Max Load: +{((plot.max()- 1)*100).round(2)}%")
        result = {"Year":year, "Morning Spike": f"+{((times[2].max()-1)*100).round(2)}%", "Mid-Day Drop from Peak": f"{(((times[2].max()-1)*100) - ((times[0].min()-1)*100)).round(2)}%", "Evening Spike": f"+{((times[1].max()-1)*100).round(2)}%"}
        output_list.append(result)

    output = pd.DataFrame(output_list)
    output = output.set_index("Year")
    print(output)
    
    #---------PLOT CUSTOMIZATION------------------
    plt.title("Normalized Day")
    plt.plot(ticks, [0 for i in range(24)], linestyle="dashed", color="gray")
    ax.set_title("India's Average Day, Normalized", fontweight="bold")
    ax.set_xlabel('Hour of day', fontweight="bold")
    ax.set_ylabel('Deviation from mean in Percentage', fontweight="bold")
    ax.set_xlim(0, 24.6)
    ax.set_xticks(ticks)
    ax.grid(axis="y", alpha=0.25, linewidth=0.6, linestyle="dashed")
    plt.legend()
    plt.savefig(f"{base_dir}/outputs/normalized_day_curves.svg")
    plt.close()

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    df = pd.read_excel(f"{base_dir}/MainData.xlsx")
    normalized_day_curves(df)