from average_day_curves import average_day_curves
from normalized_day_curves import normalized_day_curves
from demand_shock import lockdown_demand_shock, east_cyclone_demand_shock, west_cyclone_demand_shock
from pathlib import Path
import pandas as pd

#This is the main control flow. Run this program to reproduce all the GRAPHS presented in report.md

def main() -> None:
    base_dir = Path(__file__).parent
    df = pd.read_excel(f"{base_dir}/MainData.xlsx")
    while True:
        try:
            _ = input(
                """
            To generate the Average Day Curves in the National region for years(2019-2023), Enter 1
            To generate the Normalized Load Curve in the National region for the years(2019-2023), Enter 2
            To generate the Impact of COVID-19 on Electric Load, Enter 3
            To generate the Deviation from expected value curve, Enter 4
            To generate the Impact of Amphan Cyclone, Enter 5
            To generate the Impact of Nisarga Cyclone, Enter 6
            To exit the loop, Enter 7: 
        """
            )

            if int(_) not in [1, 2, 3, 4, 5, 6,7]:
                print("Enter proper data!!")

            if int(_) == 1:
                average_day_curves(df)
            elif int(_) == 2:
                normalized_day_curves(df)
            elif int(_) == 3:
                lockdown_demand_shock(df, 1)
            elif int(_) == 4:
                lockdown_demand_shock(df, 0)
            elif int(_) == 5:
                east_cyclone_demand_shock(df)
            elif int(_) == 6:
                west_cyclone_demand_shock(df)
            elif int(_) == 7:
                break

        except ValueError:
            print("Please print a number from 1 to 7! ")


if __name__ == "__main__":
    main()