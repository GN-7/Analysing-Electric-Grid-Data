# Analysing Electric Grid Data
This project aims to study the trends and behaviour of electricity consumption in India from 2019 till 2023. There are two major questions that this project answers.

### Q1.  How did India's daily load shape evolve, 2019 → 2023?
   ![Graph](assets/average_day_curves.svg)
   ![Graph2](assets/normalized_day_curves.svg)
 - Demand grew every year. But, the pattern of usage throughout the day changed with time.
 - The daily peak moved from 7PM in 2019, to 10-11AM by 2021.
 - The morning peak rose from +4.2% to +9.4%
 - The evening spike faded from +6.6% to +3.1%
    | Year | Morning Spike | Mid-Day dip from peak | Evening Spike |
    |------|---------------|-----------------------|---------------|
    | 2019 |     +4.18%    |     +2.69%            |   +6.64%      |
    | 2020 |      +7.0%    |        +6.51%         |     +5.1%     |
    | 2021 | +8.16%        |       +7.20%          | +4.99%        |
    | 2022 | +8.72%        |  +7.05%               | +4.72%        |
    | 2023 |   +9.37%      |  +8.22%               |  +3.05%       |     
  

### Q2. What do demand shocks look like in the data?
 - An unmissable demand shock was the lockdown in 2020.
   ![Lockdown](assets/lockdown_demand_shock.svg)
   ![Lockdown2](assets/lockdown_demand_deviation.svg)
 - The actual 2020 data is plotted against a growth adjusted expected value.
 - The trough, as highlighted in the graph, was on 27th March, a staggering 32.3% dip.
 - The load was below the -5% Reovery Band for 134 days of 160 days from Mar-25 to Sep 1

 - Other major supply disruptions were cuased to cyclones. Cyclone Nisarga in the West and Cyclone Amphan in the East.
 - ![Amphan](assets/east_cyclone_demand_shock.svg)
 - ![Nisarga](assets/west_cyclone_demand_shock.svg)
