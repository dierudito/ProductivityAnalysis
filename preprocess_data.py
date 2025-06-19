# Import the function from our other script
from load_data import load_data
import pandas as pd

def preprocess_data(df_time_entries, df_activities):
    """
    Cleans the dataframes and engineers new features for analysis.
    """
    print("Starting data preprocessing...")

    # --- Time Entries Preprocessing ---
    
    # 1. Convert 'WorkDate' from object (string) to datetime
    # This is crucial for any time-based analysis.
    df_time_entries['WorkDate'] = pd.to_datetime(df_time_entries['WorkDate'])

    # 2. Feature Engineering: Extract day of the week from WorkDate
    # This will allow us to analyze patterns by weekday.
    df_time_entries['DayOfWeek'] = df_time_entries['WorkDate'].dt.day_name()


    # --- Activities Preprocessing ---

    # 1. Feature Engineering: Calculate the duration of each activity
    # Subtracting two datetime columns results in a Timedelta object.
    df_activities['Duration'] = df_activities['EndDate'] - df_activities['StartDate']

    # Optional: Convert duration to a more readable format, like total hours.
    # The duration is initially a Timedelta object. We get total seconds and convert to hours.
    df_activities['Duration_Hours'] = df_activities['Duration'].dt.total_seconds() / 3600

    print("Preprocessing complete.")
    return df_time_entries, df_activities

if __name__ == '__main__':
    # 1. Load the raw data using our existing function
    raw_time_entries_df, raw_activities_df = load_data()

    # 2. Apply the preprocessing and feature engineering steps
    clean_time_entries_df, clean_activities_df = preprocess_data(
        raw_time_entries_df.copy(), # Use .copy() to avoid modifying the original df in place
        raw_activities_df.copy()
    )

    # --- Inspection of Cleaned Data ---
    print("\n\n--- Cleaned Time Entries DataFrame Info ---")
    print("Head (first 5 rows with new 'DayOfWeek' column):")
    print(clean_time_entries_df.head())
    print("\nData types and non-null values:")
    clean_time_entries_df.info()

    print("\n\n--- Cleaned Activities DataFrame Info ---")
    print("Head (first 5 rows with new 'Duration' columns):")
    # Show relevant columns to check the new features
    print(clean_activities_df[['StartDate', 'EndDate', 'Duration', 'Duration_Hours']].head())
    print("\nData types and non-null values:")
    clean_activities_df.info()