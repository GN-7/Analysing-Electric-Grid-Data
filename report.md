# Analysing Indian Electrical Load Data

### Hourly Electrical Load from 2019 to 2024

With the help of Python libraries like Pandas and MatPlotLib, the data with ~47000 rows and 4 columns was analyzed.
The results of the analysis are presented below.

First, let's define the term **Average Day**: An average day is calculated across region and time interval.
We have 24 datapoints for each day but averaging them would give us a single average load value for the day.
That value is meaningless if we want to study the pattern of consumption of electricity in a day.
So, to find what a typical day looks like, I used the following method.

Let's find out what an **Average Day** in the **West** looked like back in **2023**:


 - Reshape the data to get the load value column-wise for each hour of the day, for the whole year. Something like this: 
<img width="1427" height="402" alt="figure_1" src="https://github.com/user-attachments/assets/8f5f2071-7d68-402a-8137-6261e9a9beb1" />

