# This programs shows a line graph related to covid19 vaccinations in different countries
# pip install pandas -- used this command to install pandas in my local instance
# pip install matplotlib -- used this command to install matplotlib in my local instance
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta

# To load the data from a csv file
data = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv',
    usecols=['date', 'location', 'total_vaccinations_per_hundred'],
    parse_dates=['date'])

countries = ['United States', 'Germany', 'United Kingdom', 'Israel']  # My array to store the countries names
data = data[data['location'].isin(countries)]  # To filter data from CSV which contains my defined country names

# Summarize the data
pivot = pd.pivot_table(
    data=data,                                  # dataframe to use
    index='date',                               # The "rows" of my dataframe
    columns='location',                         # values to show as columns
    values='total_vaccinations_per_hundred',    # values to aggregate
    aggfunc='mean',                             # How to aggregate data
    )

# pivot.fillna this method is used to replace the NaN in CSV data with specified value
# Here i am using method='ffill' using as argument so
# expecting here to replace any NaN value with front record of that record
pivot = pivot.fillna(method='ffill')

# Set up key variables for the visualization
country_US = 'United States'
# To apply the color and opacity to united states country line
colors = {country:('grey' if country!= country_US else '#129583') for country in countries}
alphas = {country:(0.75 if country!= country_US else 1.0) for country in countries}

# Plot all countries
fig, axis_data = plt.subplots(figsize=(12,8))
fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
axis_data.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

for country in countries:
    axis_data.plot(
        pivot.index,              # to use as x-values
        pivot[country],           # to use as y-values
        color=colors[country],    # to color line
        alpha=alphas[country]     # transparency to use for line
    )
    axis_data.text(
        x = pivot.index[-1] + timedelta(days=2),    # to position text relative to the x-axis
        y = pivot[country].max(),                   # high to position your text
        color = colors[country],                    # color to give your text
        s = country,                                # What to write like tooltip
        alpha=alphas[country]                       # transparency to use
    )


# Configure axes
# Format what shows up on axes and how it's displayed
date_form = DateFormatter("%Y-%m-%d")
axis_data.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
axis_data.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
plt.ylim(0,100)

# Customizing axes and adding a grid
axis_data.spines['top'].set_visible(False)
axis_data.spines['right'].set_visible(False)
axis_data.spines['bottom'].set_color('#3f3f3f')
axis_data.spines['left'].set_color('#3f3f3f')
axis_data.tick_params(colors='#3f3f3f')
axis_data.grid(alpha=0.1)

# Adding a title and axis labels
plt.ylabel('Total Vaccinations per 100 People', fontsize=12, alpha=0.9)
plt.xlabel('Date', fontsize=12, alpha=0.9)
plt.title('COVID-19 Vaccinations over Time', fontsize=18, weight='bold', alpha=0.9)

# To show the graph
plt.show()
