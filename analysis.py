import pandas as pd
import plotly.express as px


# Read the data into a pandas DataFrame
df = pd.read_csv('reports.csv', header=None, names=['Index', 'Direction', 'Time1', 'Time2', 'Time3', 'Time4', 'Time5', 'Comments'])

# Parse datetime columns
for col in ['Time1', 'Time2', 'Time3', 'Time4', 'Time5']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Calculate duration between earliest and latest non-null times
def calculate_duration(row):
    times = row[['Time1', 'Time2', 'Time3', 'Time4', 'Time5']].dropna()
    if len(times) >= 2:
        duration = times.max() - times.min()
        return duration
    else:
        return pd.NaT

df['Duration'] = df.apply(calculate_duration, axis=1)

# Convert durations to total seconds
df['Duration_seconds'] = df['Duration'].dt.total_seconds()

# Extract date
df['Date'] = df['Time1'].dt.date

# Extract day of the week
df['DayOfWeek'] = df['Time1'].dt.day_name()

# Histogram of durations
fig = px.histogram(df, x='Duration_seconds', color='Direction', nbins=10, title='Histogram of Crossing Durations')
fig.update_layout(xaxis_title='Duration (seconds)', yaxis_title='Count')
fig.show()

# Box plot of durations by Direction
fig = px.box(df, x='Direction', y='Duration_seconds', points='all', title='Durations by Direction')
fig.update_layout(yaxis_title='Duration (seconds)')
fig.show()

# Number of crossings per day by Direction
crossings_per_day_dir = df.groupby(['Date', 'Direction']).size().reset_index(name='Count')

# Bar chart
fig = px.bar(crossings_per_day_dir, x='Date', y='Count', color='Direction', barmode='group', title='Number of Crossings per Day by Direction')
fig.show()

# Line plot of durations over time
fig = px.scatter(df, x='Time1', y='Duration_seconds', color='Direction', title='Crossing Durations over Time')
fig.update_layout(yaxis_title='Duration (seconds)', xaxis_title='Date')
fig.show()
