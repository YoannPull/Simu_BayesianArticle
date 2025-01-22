# Density function
import numpy as np
from scipy.stats import norm, binom, beta
from scipy.stats import beta
from scipy.optimize import bisect

import matplotlib.pyplot as plt


def standardize_binomial_distribution(n, probability, confidence_level=0.95):
    np.random.seed(42)
    # Générer directement les succès pour tous les échantillons
    binomial_samples = np.random.binomial(n=n, p=probability, size=1)

    # Calcul des statistiques
    p_hat = binomial_samples[0] / n  # Under H0 : probability = p_hat
    expected_mean = p_hat
    standard_deviation = np.sqrt(p_hat * (1 - p_hat) / n)

    # Compute confidence interval for a two-tailed test
    z_score = norm.ppf(1 - (1 - confidence_level) / 2)
    margin_of_error = z_score * standard_deviation
    confidence_interval = (expected_mean - margin_of_error, expected_mean + margin_of_error)

    return p_hat, confidence_interval


def exact_binom_distribution(n, probability, confidence_level=0.95):
    np.random.seed(42)
    # Générer une observation binomiale
    binomial_sample = np.random.binomial(n=n, p=probability)

    # Calcul de la proportion observée
    p_hat = binomial_sample / n

    # Calcul des bornes de l'intervalle de confiance exact basé sur p_hat
    alpha = 1 - confidence_level

    # Déterminer les bornes inférieure et supérieure en termes de nombre de succès
    lower_bound = binom.ppf(alpha / 2, n, p_hat) / n
    upper_bound = binom.ppf(1 - alpha / 2, n, p_hat) / n

    confidence_interval = (lower_bound, upper_bound)

    return p_hat, confidence_interval


def jeffreys_prior_posterior(n, probability, confidence_level=0.95):
    np.random.seed(42)
    """
    Computes the posterior parameters, credibility interval, and HDR for a Beta distribution
    with Jeffrey's prior and binomial observations.

    Args:
        n (int): Number of trials in the binomial distribution.
        probability (float): True probability of success in the binomial distribution.
        confidence_level (float): Confidence level for the intervals (default: 0.95).

    Returns:
        tuple: alpha_posterior, beta_posterior, credibility_interval, hdr_interval
    """
    # Generate a binomial sample
    binomial_samples = np.random.binomial(n=n, p=probability, size=1)
    nb_success = binomial_samples[0]

    # Compute posterior parameters
    alpha_prior = 0.5
    beta_prior = 0.5

    alpha_posterior = nb_success + alpha_prior
    beta_posterior = n - nb_success + beta_prior

    # Credibility interval
    alpha = 1 - confidence_level
    lower_bound = beta.ppf(alpha / 2, alpha_posterior, beta_posterior)
    upper_bound = beta.ppf(1 - alpha / 2, alpha_posterior, beta_posterior)
    credibility_interval = (lower_bound, upper_bound)

    # High-Density Region (HDR)
    def find_hdr(n, alpha_posterior, beta_posterior, confidence_level):
        """
        Computes the High-Density Region (HDR) for the Beta distribution.
        Handles potential disjoint regions for multimodal distributions.

        Args:
            alpha_posterior (float): Posterior alpha parameter.
            beta_posterior (float): Posterior beta parameter.
            confidence_level (float): Desired probability mass in the HDR.

        Returns:
            tuple: Lower and upper bounds of the HDR.
        """
        # Generate x values and compute the density
        x = np.linspace(0, 1, 100 * n)
        density = beta.pdf(x, alpha_posterior, beta_posterior)

        # Function to find the threshold
        def hdr_threshold(threshold):
            return np.trapz(density[density >= threshold], x[density >= threshold]) - confidence_level

        # Find the threshold using bisection
        threshold = bisect(hdr_threshold, 0, max(density), maxiter=10000)

        # Identify HDR regions
        hdr_regions = []
        inside_region = False
        for i in range(len(x)):
            if density[i] >= threshold:
                if not inside_region:
                    start = x[i]
                    inside_region = True
            else:
                if inside_region:
                    end = x[i - 1]
                    hdr_regions.append((start, end))
                    inside_region = False
        if inside_region:
            hdr_regions.append((start, x[-1]))

        return hdr_regions

    hdr_regions = find_hdr(n, alpha_posterior, beta_posterior, confidence_level)

    # Combine HDR regions into a single interval if unimodal
    if len(hdr_regions) == 1:
        hdr_interval = hdr_regions[0]
    else:
        # For multimodal, return the range of all HDR intervals
        hdr_interval = (hdr_regions[0][0], hdr_regions[-1][1])

    return alpha_posterior, beta_posterior, credibility_interval, hdr_interval