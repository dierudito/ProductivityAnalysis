from sqlalchemy import create_engine
import pandas as pd

# Import our custom functions
from load_data import load_data
from preprocess_data import preprocess_data

def export_analysis_results():
    """
    Runs the full pipeline and exports the aggregated insights to a SQLite database.
    """
    # --- 1. Load and Preprocess Data ---
    print("Loading and preprocessing data...")
    raw_time_entries, raw_activities = load_data()
    clean_time_entries, clean_activities = preprocess_data(
        raw_time_entries.copy(), 
        raw_activities.copy()
    )
    print("Data processing complete.")

    # --- 2. Perform Aggregations (recreating our insights) ---
    print("Aggregating insights...")
    
    # Insight 1: Total hours per activity
    activity_total_hours = clean_activities.groupby('ActivityLabel')['Duration_Hours'].sum().reset_index()
    activity_total_hours = activity_total_hours.sort_values(by='Duration_Hours', ascending=False)
    
    # Insight 2: Total productive hours per weekday
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    activities_with_day = clean_activities.copy()
    activities_with_day['DayOfWeek'] = activities_with_day['StartDate'].dt.day_name()
    activities_with_day['DayOfWeek'] = pd.Categorical(activities_with_day['DayOfWeek'], categories=weekday_order, ordered=True)
    productive_hours_by_day = activities_with_day.groupby('DayOfWeek')['Duration_Hours'].sum().reset_index()

    # --- 3. Export to Database ---
    print("Connecting to SQLite database and exporting tables...")
    
    # Create a database engine. This will create the file 'insights.db' if it doesn't exist.
    engine = create_engine('sqlite:///insights.db')

    # Use the to_sql() method to save the DataFrames as tables
    activity_total_hours.to_sql(
        name='activity_summary', 
        con=engine, 
        if_exists='replace', 
        index=False
    )

    productive_hours_by_day.to_sql(
        name='daily_productivity_summary', 
        con=engine, 
        if_exists='replace', 
        index=False
    )
    
    print("\nExport complete. Insights are saved in 'insights.db'.")
    print("Tables created: 'activity_summary', 'daily_productivity_summary'")


if __name__ == '__main__':
    export_analysis_results()