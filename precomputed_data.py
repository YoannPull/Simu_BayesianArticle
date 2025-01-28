import os
from utils.plotter import generate_dash_plots

# Define scenarios
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

# Create directory for JPEG files
# os.makedirs("plots", exist_ok=True)

# Generate and save plots
for scenario in scenarios:
    n, p, confidence, name = scenario["n"], scenario["p"], scenario["confidence_level"], scenario["scenario_name"]
    fig_normal, fig_exact, fig_bayesian = generate_dash_plots(n, p, confidence)

    # Save each plot as a JPEG file
    fig_normal.write_image(f"assets/plots/{name}_normal.jpeg", format="jpeg", width=800, height=600)
    fig_exact.write_image(f"assets/plots/{name}_exact.jpeg", format="jpeg", width=800, height=600)
    fig_bayesian.write_image(f"assets/plots/{name}_bayesian.jpeg", format="jpeg", width=800, height=600)
