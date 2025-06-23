from predictive_analysis import run_prediction_model
from export_insights import export_analysis_results
import time

def main():
    """
    Main pipeline execution function.
    """
    print(f"--- Pipeline started at {time.ctime()} ---")
    
    print("\n>>> Running Predictive Analysis and Model Training...")
    try:
        run_prediction_model()
        print(">>> Predictive Analysis completed successfully.")
    except Exception as e:
        print(f"!!! An error occurred during predictive analysis: {e}")

    print("\n>>> Running Insight Export...")
    try:
        export_analysis_results()
        print(">>> Insight Export completed successfully.")
    except Exception as e:
        print(f"!!! An error occurred during insight export: {e}")

    print(f"\n--- Pipeline finished at {time.ctime()} ---")


if __name__ == '__main__':
    main()