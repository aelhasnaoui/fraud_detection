import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from joblib import dump
import matplotlib.pyplot as plt
import os
import seaborn as sns

def train_model(data_file, model_file, output_dir):
    # Load processed data
    df = pd.read_csv(data_file)

    # Separate features and target
    X = df.drop(columns=["Class"])
    y = df["Class"]

    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    dump(model, model_file)
    print(f"Model saved to {model_file}")

    # Generate visualizations
    os.makedirs(output_dir, exist_ok=True)

    # Feature Importance
    feature_importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importance.values, y=feature_importance.index)
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "feature_importance.png"))
    plt.close()

    # Confusion Matrix (Fixed)
    y_pred = model.predict(X_test)
    plt.figure(figsize=(6, 6))
    disp = ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close()

    # Class Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x="Class", data=df)
    plt.title("Class Distribution")
    plt.savefig(os.path.join(output_dir, "class_distribution.png"))
    plt.close()

if __name__ == "__main__":
    data_file = "data/processed_data.csv"
    model_file = "models/random_forest_model.pkl"
    output_dir = "results"
    train_model(data_file, model_file, output_dir)
