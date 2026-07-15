import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")

df = df.set_index("datetime")
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
