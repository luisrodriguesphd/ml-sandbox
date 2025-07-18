# 📊 Linear Regression: Impact of Feature Scaling and Transformations

This experiment explores how **feature scaling** and **nonlinear transformations** affect the performance and behavior of linear regression models, both with and without regularization.

---

## 🎯 Objectives

- Demonstrate that **linear transformations** (e.g., z-score normalization) do not impact model performance in Ordinary Least Squares (OLS).
- Show that **nonlinear transformations** (e.g., square root) change the relationship between the feature and the target, altering predictions and model fit.
- Analyze how **Ridge regularization** interacts with unscaled features.

---

## 📁 Files

- `start.cmd`: Windows setup script that creates a virtual environment and installs requirements automatically.
- `notebook.ipynb`: Interactive version of the experiment.
- `code.py`: Standalone script to run the experiment.
- `requirements.txt`: Dependencies needed to run the code.

---

## 📈 Suggested Extensions

- Add Lasso (L1) regularization and compare results.
- Visualize residuals for different transformations.
- Try other transformations like `log(x)` or `x²` and evaluate performance.
