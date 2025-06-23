import pandas as pd
import numpy as np

# Import the function from our other script
from load_data import load_data

def preprocess_data(df_time_entries, df_activities):
    """
    Cleans the dataframes and engineers new features for analysis.
    """
    print("Starting data preprocessing...")

    # --- Time Entries Preprocessing ---
    df_time_entries['WorkDate'] = pd.to_datetime(df_time_entries['WorkDate'])
    df_time_entries['DayOfWeek'] = df_time_entries['WorkDate'].dt.day_name()

    # --- Activities Preprocessing ---
    df_activities['Duration'] = df_activities['EndDate'] - df_activities['StartDate']
    df_activities['Duration_Hours'] = df_activities['Duration'].dt.total_seconds() / 3600
    df_activities['DayOfWeek'] = df_activities['StartDate'].dt.day_name()
    df_activities['Description'] = df_activities['Description'].fillna('')
    
    # Now, create the new 'ActivityLabel' column.
    # We use np.where for efficient, vectorized if/else logic.
    # Condition: Is the 'Description' column not an empty string?
    # If true:  Combine CardCode and Description.
    # If false: Use only the CardCode.
    df_activities['ActivityLabel'] = np.where(
        df_activities['Description'] != '',
        df_activities['CardCode'].astype(str) + ' - ' + df_activities['Description'],
        df_activities['CardCode'].astype(str)
    )

    print("Preprocessing complete.")
    return df_time_entries, df_activities

if __name__ == '__main__':
    # (The rest of this file for testing remains the same)
    raw_time_entries_df, raw_activities_df = load_data()
    clean_time_entries_df, clean_activities_df = preprocess_data(
        raw_time_entries_df.copy(),
        raw_activities_df.copy()
    )

    print("\n\n--- Cleaned Activities DataFrame Info ---")
    # Let's check our new 'ActivityLabel' column
    print(clean_activities_df[['CardCode', 'Description', 'ActivityLabel']].head(10))
    print("\nData types:")
    clean_activities_df.info()