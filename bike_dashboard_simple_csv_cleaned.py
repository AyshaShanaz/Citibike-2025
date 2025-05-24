#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Load the cleaned Citibike CSV file
describe = ''
import pandas as pd
import os

csv_file = '202201-citibike-tripdata_1_cleaned.csv'
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    # Standardize column names to match expected format
    df.rename(columns={'started_at':'start_time','ended_at':'end_time','member_casual':'user_type'}, inplace=True)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    print('Loaded cleaned CSV successfully. DataFrame shape:', df.shape)
    print('Columns:', list(df.columns))
    print(df.head())
    describe = df.describe(include='all')
    print(describe)
else:
    print('Cleaned CSV file not found. Please upload 202201-citibike-tripdata_1_cleaned.csv to the same directory as this notebook.')


# In[8]:


# Cell 1: import libraries and load data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load cleaned trip data (ensure this CSV is in the same folder)
df = pd.read_csv("cleaned_bikeshare.csv", parse_dates=["start_time", "end_time"])

# Load daily temperature data
temps = pd.read_csv("daily_temps.csv", parse_dates=["date"])

# Quick peek at the trips DataFrame
print(df.head())


# In[14]:


# Cell 3: aggregate daily trip counts
daily = (
    df
    .assign(date=df.start_time.dt.date)
    .groupby("date")
    .size()
    .rename("trips")
    .reset_index()
)

# Convert the date column to datetime64[ns] type to match temps DataFrame
daily['date'] = pd.to_datetime(daily['date'])

# Alternatively, if you want to convert temps DataFrame's date column to match daily
# temps['date'] = temps['date'].dt.date  # Use this if temps['date'] is datetime

# Merge with temperature data
merged = daily.merge(temps, on="date")

# Preview the merged DataFrame
print(merged.head())


# In[11]:


# First, define the merged DataFrame
# This is a placeholder - you need to replace this with your actual data loading/merging code
import pandas as pd
import plotly.graph_objects as go

# Example of how to create the merged DataFrame (replace with your actual data source)
# For example:
# merged = pd.read_csv('your_data.csv')
# OR
# merged = pd.merge(trips_df, temperature_df, on='date')

# For demonstration, creating sample data
dates = pd.date_range(start='2023-01-01', periods=30)
trips = [1000 + i*50 + (i**2)*2 for i in range(30)]
temps = [5 + i*0.5 for i in range(30)]
merged = pd.DataFrame({
    'date': dates,
    'trips': trips,
    'avg_temp': temps
})

# Now create the dual-axis line chart
fig_line = go.Figure()

# Trace for daily trips (left y-axis)
fig_line.add_trace(
    go.Scatter(
        x=merged.date, 
        y=merged.trips, 
        name="Daily Trips", 
        line=dict(color="royalblue")
    )
)

# Trace for average temperature (right y-axis)
fig_line.add_trace(
    go.Scatter(
        x=merged.date, 
        y=merged.avg_temp, 
        name="Avg Temp (°C)", 
        line=dict(color="firebrick"),
        yaxis="y2"
    )
)

# Configure layout with two y-axes
fig_line.update_layout(
    title="Daily Citi Bike Trips vs. Average Temperature",
    xaxis_title="Date",
    yaxis=dict(title="Number of Trips", side="left"),
    yaxis2=dict(
        title="Temp (°C)", 
        overlaying="y", 
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    margin=dict(l=50, r=50, t=60, b=50)
)

# Display the interactive dual-axis chart
fig_line.show()


# In[13]:


# Handle missing daily_temps.csv and plot top stations without errors
import pandas as pd, os
import plotly.express as px

# Assume df is already defined
# Load temperatures if available
if os.path.exists('daily_temps.csv'):
    temps = pd.read_csv('daily_temps.csv', parse_dates=['date'])
    # Convert start_time to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df['start_time']):
        df['start_time'] = pd.to_datetime(df['start_time'])
    
    # Extract date from start_time and convert to same type as temps['date']
    df['trip_date'] = df['start_time'].dt.date
    df['trip_date'] = pd.to_datetime(df['trip_date'])  # Convert to datetime64[ns]
    
    # Ensure both columns are the same type before merging
    merged = pd.merge(df, temps, left_on='trip_date', right_on='date', how='left')
    print('Merged with temps:', merged.shape)
else:
    print('daily_temps.csv not found, using df only')
    merged = df.copy()

# Count trips per start station
station_counts = merged.groupby('start_station_name').size().reset_index(name='count')
# Display top 5
print(station_counts.sort_values('count', ascending=False).head())

# Plot top 10 stations
top10 = station_counts.sort_values('count', ascending=False).head(10)
fig = px.bar(top10, x='start_station_name', y='count', title='Top 10 Start Stations')
fig.show()


# In[ ]:




