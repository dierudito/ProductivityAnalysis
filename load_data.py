import pandas as pd
import pyodbc
import sys

# --- Configuration ---
# TODO: Replace with your actual server name and database name
# For a local SQL Express instance, it's often 'localhost\SQLEXPRESS' or '.\SQLEXPRESS'
SERVER_NAME = 'localhost'  # Example: 'LAPTOP-XYZ\SQLEXPRESS'
DATABASE_NAME = 'PulseShift'        # Example: 'TimeTrackingDB'
DRIVER = '{ODBC Driver 17 for SQL Server}' # This is standard, usually doesn't need to change

# Connection string using Windows Authentication
# A "trusted connection" doesn't require a username/password when you're logged into Windows
conn_string = f'DRIVER={DRIVER};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'

# --- SQL Queries ---
# Query for time entries. We'll select only the necessary columns.
query_time_entries = """
SELECT
    Id,
    EntryType,
    EntryDate,
    WorkDate
FROM
    TimeEntries
WHERE
    IsDeleted = 0;
"""

# Query for activities, flattened with their periods.
# This join is crucial to "flatten" the nested data structure into a tabular format.
# It's more efficient to do this join in SQL than in Python.
query_activities = """
SELECT
    a.Id AS ActivityId,
    a.Description,
    a.CardCode,
    ap.Id AS ActivityPeriodId,
    ap.StartDate,
    ap.EndDate
FROM
    Activities a
JOIN
    ActivityPeriods ap ON a.Id = ap.ActivityId
WHERE
    a.IsDeleted = 0 AND ap.IsDeleted = 0;
"""

def load_data():
    """
    Connects to the SQL Server database and loads the data
    into pandas DataFrames.
    """
    conn = None  # Initialize connection to None
    try:
        # Establish the database connection
        print("Connecting to the database...")
        conn = pyodbc.connect(conn_string)
        print("Connection successful.")

        # Load data using pandas' read_sql_query function
        print("Loading TimeEntries...")
        df_time_entries = pd.read_sql_query(query_time_entries, conn)

        print("Loading Activities...")
        df_activities = pd.read_sql_query(query_activities, conn)
        
        print("\n--- Data Loading Complete ---")
        return df_time_entries, df_activities

    except pyodbc.Error as ex:
        # Handle potential connection or query errors
        sqlstate = ex.args[0]
        print(f"Database Error Occurred: {sqlstate}")
        print(ex)
        sys.exit(1) # Exit the script if we can't load data
        
    finally:
        # Ensure the connection is always closed
        if conn:
            print("Closing database connection.")
            conn.close()

if __name__ == '__main__':
    # This block runs when the script is executed directly
    time_entries_df, activities_df = load_data()

    # --- Initial Data Inspection ---
    print("\n--- Time Entries DataFrame Info ---")
    print(f"Shape: {time_entries_df.shape}") # (rows, columns)
    print("Head (first 5 rows):")
    print(time_entries_df.head())
    print("\nData types and non-null values:")
    time_entries_df.info()

    print("\n\n--- Activities DataFrame Info ---")
    print(f"Shape: {activities_df.shape}")
    print("Head (first 5 rows):")
    print(activities_df.head())
    print("\nData types and non-null values:")
    activities_df.info()