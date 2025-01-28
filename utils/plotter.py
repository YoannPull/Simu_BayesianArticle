import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm, binom, beta
from utils.calculations import (
    standardize_binomial_distribution,
    exact_binom_distribution,
    jeffreys_prior_posterior,
)
def generate_dash_plots(n, probability, confidence_level=0.95):
    # Calculate distributions and intervals
    p_hat_normal, ci_normal = standardize_binomial_distribution(n, probability, confidence_level)
    p_hat_exact, ci_exact = exact_binom_distribution(n, probability, confidence_level)
    alpha_post, beta_post, ci_bayesian, hdr_bayesian = jeffreys_prior_posterior(n, probability, confidence_level)

    x_normal = np.linspace(0, 1, n * 10)
    x_beta = np.linspace(0, 1, n * 10)

    # Zoom range for plots
    zoom_lower = max(0, probability - 3 / np.sqrt(n))
    zoom_upper = min(1, probability + 3 / np.sqrt(n))

    # Plot 1: Normal Approximation
    normal_density = norm.pdf(x_normal, loc=p_hat_normal, scale=np.sqrt(p_hat_normal * (1 - p_hat_normal) / n))
    fig_normal = go.Figure()
    fig_normal.add_trace(go.Scatter(
        x=x_normal,
        y=normal_density,
        mode="lines",
        name="Normal Approximation",
        line=dict(color="blue", width=2),
    ))
    fig_normal.add_vline(x=ci_normal[0], line=dict(color="blue", dash="dash"), annotation_text="CI Lower", annotation_position="top left")
    fig_normal.add_vline(x=ci_normal[1], line=dict(color="blue", dash="dash"), annotation_text="CI Upper", annotation_position="top right")
    fig_normal.update_layout(
        title=f"Normal Approximation (n={n}, p={probability}, CI={confidence_level * 100:.1f}%)",
        xaxis_title="Proportion",
        yaxis_title="Density",
        xaxis=dict(range=[zoom_lower, zoom_upper]),
        template="plotly_white",
    )

    # Plot 2: Exact Binomial Distribution
    exact_density = binom.pmf(np.arange(n + 1), n, p_hat_exact) * n
    fig_exact = go.Figure()
    fig_exact.add_trace(go.Scatter(
        x=np.arange(n + 1) / n,
        y=exact_density,
        mode="markers+lines",
        name="Exact Binomial",
        line=dict(color="green"),
        marker=dict(size=8),
    ))
    fig_exact.add_vline(x=ci_exact[0], line=dict(color="green", dash="dash"), annotation_text="CI Lower", annotation_position="top left")
    fig_exact.add_vline(x=ci_exact[1], line=dict(color="green", dash="dash"), annotation_text="CI Upper", annotation_position="top right")
    fig_exact.update_layout(
        title=f"Exact Binomial Distribution (n={n}, p={probability}, CI={confidence_level * 100:.1f}%)",
        xaxis_title="Proportion",
        yaxis_title="Density",
        xaxis=dict(range=[zoom_lower, zoom_upper]),
        template="plotly_white",
    )

    # Plot 3: Bayesian Posterior
    bayesian_density = beta.pdf(x_beta, alpha_post, beta_post)
    fig_bayesian = go.Figure()
    fig_bayesian.add_trace(go.Scatter(
        x=x_beta,
        y=bayesian_density,
        mode="lines",
        name="Bayesian Posterior",
        line=dict(color="red", width=2),
    ))
    fig_bayesian.add_vline(x=ci_bayesian[0], line=dict(color="red", dash="dash"), annotation_text="CI Lower", annotation_position="top left")
    fig_bayesian.add_vline(x=ci_bayesian[1], line=dict(color="red", dash="dash"), annotation_text="CI Upper", annotation_position="top right")
    fig_bayesian.add_vline(x=hdr_bayesian[0], line=dict(color="red", dash="dot"), annotation_text="HDR Lower", annotation_position="bottom left")
    fig_bayesian.add_vline(x=hdr_bayesian[1], line=dict(color="red", dash="dot"), annotation_text="HDR Upper", annotation_position="bottom right")
    fig_bayesian.update_layout(
        title=f"Bayesian Posterior (n={n}, p={probability}, CI={confidence_level * 100:.1f}%)",
        xaxis_title="Proportion",
        yaxis_title="Density",
        xaxis=dict(range=[zoom_lower, zoom_upper]),
        template="plotly_white",
    )

    return fig_normal, fig_exact, fig_bayesian
    fig = go.Figure()

    # Normal approximation
    normal_density = norm.pdf(x_normal, loc=p_hat_normal, scale=np.sqrt(p_hat_normal * (1 - p_hat_normal) / n))
    fig.add_trace(go.Scatter(
        x=x_normal,
        y=normal_density,
        mode="lines",
        name="Normal Approximation",
        line=dict(color="blue", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=[ci_normal[0], ci_normal[1]],
        y=[0, 0],
        mode="markers+text",
        text=["Lower CI", "Upper CI"],
        name="Normal CI",
        marker=dict(color="blue", size=10),
    ))

    # Exact binomial distribution
    exact_density = binom.pmf(np.arange(n + 1), n, p_hat_exact) * n
    fig.add_trace(go.Scatter(
        x=np.arange(n + 1) / n,
        y=exact_density,
        mode="markers",
        name="Exact Binomial",
        marker=dict(color="green", size=8),
    ))
    fig.add_trace(go.Scatter(
        x=[ci_exact[0], ci_exact[1]],
        y=[0, 0],
        mode="markers+text",
        text=["Lower CI", "Upper CI"],
        name="Exact CI",
        marker=dict(color="green", size=10),
    ))

    # Bayesian posterior
    bayesian_density = beta.pdf(x_beta, alpha_post, beta_post)
    fig.add_trace(go.Scatter(
        x=x_beta,
        y=bayesian_density,
        mode="lines",
        name="Bayesian Posterior",
        line=dict(color="red", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=[ci_bayesian[0], ci_bayesian[1]],
        y=[0, 0],
        mode="markers+text",
        text=["Lower CI", "Upper CI"],
        name="Bayesian CI",
        marker=dict(color="red", size=10),
    ))
    fig.add_trace(go.Scatter(
        x=[hdr_bayesian[0], hdr_bayesian[1]],
        y=[0, 0],
        mode="markers+text",
        text=["HDR Lower", "HDR Upper"],
        name="Bayesian HDR",
        marker=dict(color="red", symbol="star", size=12),
    ))

    # Mise en page
    fig.update_layout(
        title=f"Probability Distributions (n={n}, p={probability}, CI={confidence_level * 100:.1f}%)",
        xaxis_title="Proportion",
        yaxis_title="Density",
        legend_title="Distributions",
        xaxis=dict(range=[zoom_lower, zoom_upper]),
        template="plotly_white",
    )

    return fig