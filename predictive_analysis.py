import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

# Import our custom data loading and preprocessing functions
from load_data import load_data
from preprocess_data import preprocess_data

def run_prediction_model():
    """
    Full pipeline to train and evaluate a model that predicts activity duration.
    """
    # --- 1. Load and Preprocess Data ---
    # This leverages all the work we've done so far!
    print("Loading and preprocessing data...")
    raw_time_entries, raw_activities = load_data()
    _, clean_activities = preprocess_data(raw_time_entries.copy(), raw_activities.copy())

    # For prediction, let's filter out extremely long tasks that might be data errors
    # or very rare events, as they can skew the model's learning.
    # Here, we keep tasks that are less than 40 hours long.
    clean_activities = clean_activities[clean_activities['Duration_Hours'] < 40]
    print(f"Using {len(clean_activities)} records for training after filtering outliers.")

    # --- 2. Feature Engineering & Selection ---
    # Define what we use to predict (features, X) and what we want to predict (target, y).
    features = ['ActivityLabel', 'DayOfWeek']
    target = 'Duration_Hours'

    X = clean_activities[features]
    y = clean_activities[target]

    # --- 3. Convert Categorical Features to Numbers ---
    # ML models only understand numbers. We use One-Hot Encoding to convert text columns.
    print("Performing One-Hot Encoding on features...")
    X_encoded = pd.get_dummies(X, columns=['ActivityLabel', 'DayOfWeek'], drop_first=True)

    # --- 4. Split Data into Training and Testing Sets ---
    # The GOLDEN RULE of ML: Never test your model on the data it was trained on.
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )

    # --- 5. Choose and Train the Model ---
    print("Training the RandomForestRegressor model...")
    # We choose RandomForest because it's powerful, versatile, and doesn't require feature scaling.
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    
    # The .fit() method is where the model "learns" from the data.
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 6. Make Predictions on the Test Set ---
    print("Making predictions on the unseen test data...")
    predictions = model.predict(X_test)

    # --- 7. Evaluate Model Performance ---
    print("\n--- Model Evaluation ---")
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"Mean Absolute Error (MAE): {mae:.2f} hours")
    print(f"R-squared (R²): {r2:.2f}")

    # --- 8. (Bonus) Feature Importance ---
    # Let's see what the model thought was most important.
    print("\n--- Top 10 Most Important Features ---")
    importances = pd.Series(model.feature_importances_, index=X_encoded.columns)
    print(importances.nlargest(10))


if __name__ == '__main__':
    run_prediction_model()