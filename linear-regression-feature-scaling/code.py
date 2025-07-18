"""
linear-regression-scaling: Investigates the impact of feature scaling and transformations
on OLS and Ridge regression performance.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

def generate_data(n=1000, seed=42):
    np.random.seed(seed)
    x1 = np.random.uniform(0, 10, size=n)
    x2 = np.random.normal(0, 10, size=n)
    noise = np.random.normal(0, 5, size=n)
    y = 10 * x1**2 + 3 * x2 + noise
    X_orig = np.column_stack((x1, x2))
    X_sqrt = np.column_stack((np.sqrt(x1), x2))
    X_scaled = np.column_stack((100 * (x1 - 2), x2))
    return X_orig, X_sqrt, X_scaled, y

def evaluate_model(X, y, model_name="Model", model_type="ols"):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    if model_type == "ridge":
        model = Ridge(alpha=2.0)
    else:
        model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"==== {model_name} ====")
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    print("R^2 Score:", r2_score(y_test, y_pred))
    print("RMSE:", root_mean_squared_error(y_test, y_pred))
    return y_test, y_pred

def plot_predictions(y_test, predictions_dict):
    plt.figure(figsize=(12, 10))
    for i, (title, y_pred) in enumerate(predictions_dict.items()):
        plt.subplot(2, 2, i + 1)
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.title(title)
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    X_orig, X_sqrt, X_scaled, y = generate_data()
    y_test1, y_pred1 = evaluate_model(X_orig, y, "OLS with x1 (original)")
    y_test2, y_pred2 = evaluate_model(X_sqrt, y, "OLS with x1' = sqrt(x1)")
    y_test3, y_pred3 = evaluate_model(X_scaled, y, "OLS with x1' = 100 *  (x1 - 2)")
    y_test4, y_pred4 = evaluate_model(X_scaled, y, "Ridge with x1' = 100 *  (x1 - 2)", model_type="ridge")

    predictions = {
        "OLS with x1 (original)": y_pred1,
        "OLS with x1' = sqrt(x1)": y_pred2,
        "OLS with x1' = 100 * (x1 - 2)": y_pred3,
        "Ridge with x1' = 100 * (x1 - 2)": y_pred4,
    }

    plot_predictions(y_test1, predictions)
