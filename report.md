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
![Figure of the dataframe](/assets/figure_1.png)

 - Now, we take an average, but column-wise. This way we can get the average load at each time of the day.
   24 values, each corresponding to an hour of the day.
![Figure of average data](/assets/figure_2.png)

 - Plotting it using MatPlotLib, we get:
   ![Plot of the above values](/assets/figure_3.png)

   ## Load Curves of the Average Day(2019-2023)

   Plotting the evolution of the **Average Day** Load curves from 2019 to 2023 for the whole country looks like this:
   ![Plot of load curves](/assets/figure_4.png)

   ### Inferences drawn from the load curves

    - The average load is increasing significantly year-on-year.(Except 2020, This anomaly is taken care of later on.)
    - Though the overall magnitude of the load is increasing, the shape of the curve remains constant.
    - The peak hours of the day are 10AM - 12PM consistently.
    - After 12PM, heading into the afternoon, a decline in the load can be observed.
    - Later in the evening, it spikes up and settles down at a low by the end of the night.
