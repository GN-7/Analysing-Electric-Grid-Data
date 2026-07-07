import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#Accessing The Data
base_dir = Path(__file__).parent
df = pd.read_excel(f"{base_dir}/MainData.xlsx")


#Seperating Date and Time from Timestamp format

df['Dates'] = pd.to_datetime(df['datetime']).dt.date
df['Time'] = pd.to_datetime(df['datetime']).dt.time
df = df.drop(columns="datetime")




