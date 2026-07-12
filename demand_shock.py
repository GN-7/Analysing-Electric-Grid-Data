import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import numpy as np
#------------ACCESSING THE RAW DATA--------------------------
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")



daily_mean = df.set_index("datetime")["National"].resample("D").mean()

monthly_mean = daily_mean.resample("MS").mean()

drop_percent = ((monthly_mean['2019'].values - monthly_mean["2020"].values)/monthly_mean['2019'])*100

print(monthly_mean["2019"][0:3])
print(monthly_mean["2020"][0:3])
plt.plot([i + 1 for i in range(12)], monthly_mean[0:12], marker="o")
plt.plot([i + 1 for i in range(12)], monthly_mean[12:24], marker="o")
plt.plot([i + 1 for i in range(12)], monthly_mean[0:12].values * 1.00458)
plt.xticks([i + 1 for i in range(12)])
plt.show()