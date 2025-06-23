import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import our custom functions
from load_data import load_data
from preprocess_data import preprocess_data

def run_analysis():
    """
    Main function to run the full analysis pipeline.
    """
    # 1. Load and preprocess data
    raw_time_entries, raw_activities = load_data()
    clean_time_entries, clean_activities = preprocess_data(
        raw_time_entries.copy(), 
        raw_activities.copy()
    )

    # --- Analysis Question 1: Which activities take the most time? ---
    print("\n--- Analyzing Activity Durations ---")
    
    activity_total_hours = clean_activities.groupby('ActivityLabel')['Duration_Hours'].sum().sort_values(ascending=False)
    
    print("Total hours per activity:")
    print(activity_total_hours.head(10)) # Print top 10

    # Visualization 1: Bar chart of total hours per activity (Top 15)
    plt.figure(figsize=(12, 8)) # Create a figure to draw on
    sns.barplot(x=activity_total_hours.head(15).values, y=activity_total_hours.head(15).index, orient='h')
    plt.title('Top 15 Most Time-Consuming Activities', fontsize=16)
    plt.xlabel('Total Hours Logged', fontsize=12)
    plt.ylabel('Activity Description', fontsize=12)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    plt.show() # Display the plot


    # --- Analysis Question 2: What is the frequency of time entries per weekday? ---
    print("\n--- Analyzing Time Entry Frequency by Weekday ---")
    
    # Define the logical order for the days of the week
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    clean_time_entries['DayOfWeek'] = pd.Categorical(clean_time_entries['DayOfWeek'], categories=weekday_order, ordered=True)
    
    day_counts = clean_time_entries['DayOfWeek'].value_counts().sort_index()
    print("Number of time entries per day:")
    print(day_counts)

    # Visualization 2: Bar chart of entries per day
    plt.figure(figsize=(10, 6))
    sns.barplot(x=day_counts.index, y=day_counts.values)
    plt.title('Total Time Entries (ClockIn/Out, etc.) by Day of Week', fontsize=16)
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Number of Entries', fontsize=12)
    plt.show()


    # --- Analysis Question 3: How are productive hours distributed across the week? ---
    print("\n--- Analyzing Total Productive Hours by Weekday ---")

    # To link activity hours to a weekday, we can use the StartDate of the activity
    activities_with_day = clean_activities.copy()
    activities_with_day['DayOfWeek'] = activities_with_day['StartDate'].dt.day_name()
    activities_with_day['DayOfWeek'] = pd.Categorical(activities_with_day['DayOfWeek'], categories=weekday_order, ordered=True)
    
    # Group by weekday and sum the hours
    productive_hours_by_day = activities_with_day.groupby('DayOfWeek')['Duration_Hours'].sum().sort_index()
    print("Total productive hours logged per day:")
    print(productive_hours_by_day)

    # Visualization 3: Bar chart of productive hours
    plt.figure(figsize=(10, 6))
    sns.barplot(x=productive_hours_by_day.index, y=productive_hours_by_day.values)
    plt.title('Total Productive Hours Logged by Day of Week', fontsize=16)
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Total Hours', fontsize=12)
    plt.show()


if __name__ == '__main__':
    run_analysis()