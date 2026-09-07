# Option Pricing Engine

## Overview

A Python option pricing engine implementing analytical and numerical methods for pricing European, American and path-dependent options.

The project implements Black-Scholes, binomial tree and Monte Carlo pricing, with analysis of numerical convergence, Monte Carlo estimation error and variance reduction. It also demonstrates the use of path simulation for pricing an up-and-out barrier option.

## Features

- Black-Scholes pricing for European call and put options
- Binomial tree pricing for European and American options
- Monte Carlo pricing for European call and put options
- Antithetic variates for Monte Carlo variance reduction
- Path-based Monte Carlo pricing of an up-and-out barrier call
- Historical volatility estimation using market data
- Analysis of binomial and Monte Carlo convergence to Black-Scholes
- Analysis of Monte Carlo standard error and variance reduction
- Automated tests for the pricing models

## Models

### Black-Scholes

Provides closed-form pricing for European call and put options and serves as an analytical benchmark for the numerical pricing methods.

### Binomial Tree

Uses a discrete-time risk-neutral stock price tree and backward induction to price European and American options. American options account for the possibility of early exercise at each node.

### Monte Carlo

Simulates terminal stock prices under geometric Brownian motion and estimates European option values from discounted expected payoffs. Antithetic variates are implemented to reduce estimator variance.

For path-dependent options, full stock price paths can be simulated over discrete time steps. This is used to price an up-and-out barrier call.

## Project Structure

```text
option-pricing-engine/
├── notebooks/
│   └── option_pricing_analysis.ipynb
├── src/
│   └── option_pricing/
│       ├── __init__.py
│       ├── options.py
│       ├── black_scholes.py
│       ├── binomial.py
│       └── monte_carlo.py
├── tests/
│   ├── test_black_scholes.py
│   ├── test_binomial.py
│   └── test_monte_carlo.py
├── pyproject.toml
├── requirements.txt
└── README.md