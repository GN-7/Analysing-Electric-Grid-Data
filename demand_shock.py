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
ticks = pd.date_range("01-01-2019", "16-03-2019", freq="h", inclusive="left").hour.astype(str)


pivoted_region = pd.pivot_table(df, index=["Dates"], columns="Time", values="National")

#DataFrame not Pivot Table
'''df_national_2019 = pivoted_region.loc[datetime.date(2019, 1, 1):datetime.date(2019, 3, 15)] 
df_national_2020 = pivoted_region.loc[datetime.date(2020, 1, 1):datetime.date(2020, 3, 15)]'''
plt.show()