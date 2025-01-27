import json
from utils.plotter import generate_dash_plots
import numpy as np

# Define scenarios the different scenarios based on the articles
scenarios = [
    {"n": 1000, "p": 0.01, "confidence_level": 0.95, "scenario_name": "baseline 1"},
    {"n": 1000, "p": 0.05, "confidence_level": 0.95, "scenario_name": "baseline 2"},
    {"n": 1000, "p": 0.001, "confidence_level": 0.95, "scenario_name": "low default portfolio 1"},
    {"n": 1000, "p": 0.005, "confidence_level": 0.95, "scenario_name": "low default portfolio 2"},
    {"n": 100, "p": 0.01, "confidence_level": 0.95, "scenario_name": "small sample 1"},
    {"n": 100, "p": 0.05, "confidence_level": 0.95, "scenario_name": "small sample 2"},
    {"n": 100_000, "p": 0.01, "confidence_level": 0.95, "scenario_name": "large sample 1"},
    {"n": 100_000, "p": 0.05, "confidence_level": 0.95, "scenario_name": "large sample 2"},
    {"n": 500_000, "p": 0.01, "confidence_level": 0.95, "scenario_name": "large sample 3"},
]

# Precompute results
def convert_to_serializable(obj):
    """Recursively convert numpy objects to native Python types."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    return obj

precomputed_results = {}
for scenario in scenarios:
    n = scenario["n"]
    p = scenario["p"]
    confidence = scenario["confidence_level"]
    name = scenario["scenario_name"]

    # Generate plots
    fig_normal, fig_exact, fig_bayesian = generate_dash_plots(n, p, confidence)

    # Convert figures to JSON and ensure they're serializable
    precomputed_results[name] = {
        "n": n,
        "p": p,
        "confidence_level": confidence,
        "normal_plot": convert_to_serializable(fig_normal.to_plotly_json()),
        "exact_plot": convert_to_serializable(fig_exact.to_plotly_json()),
        "bayesian_plot": convert_to_serializable(fig_bayesian.to_plotly_json()),
    }

# Save to JSON file
with open("precomputed_results.json", "w") as f:
    json.dump(precomputed_results, f)

print("Precomputed results saved successfully to 'precomputed_results.json'.")
