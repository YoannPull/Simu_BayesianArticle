from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    """Define the overall layout of the app."""
    return dbc.Container([
        # Navigation Bar
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/", id="home-link")),
                dbc.NavItem(dbc.NavLink("Graphing", href="/graph", id="graph-link"))
            ],
            brand="Confidence Interval Comparison",  # App name
            brand_href="/",
            color="#404140",  # Dark gray background
            dark=True,
        ),

        # Content container
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content")
    ], fluid=True)


from dash import dcc, html
import dash_bootstrap_components as dbc

def home_page():
    """Layout for the Home Page."""
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to Confidence Interval Comparison", className="text-center mb-4 text-primary"), width=12)
        ]),
        dbc.Row([
            dbc.Col(dcc.Markdown(
                r"""
                This application provides a platform to explore and compare confidence and credibility intervals using simulated data.

                ### How It Works
                - The parameters n (number of trials) and  p  (probability of success) are used to generate observations following a Bernoulli process (1 for success, 0 for failure).
                - In real-world scenarios, these observations would come from actual experiments or data collection.
                - A commonly used method to estimate the theoretical probability of success is:
                  $$
                  \hat{p} = \frac{\sum Y_i}{n}
                  $$
                  where Y_i  represents individual Bernoulli trials.

                ### Key Details
                - The estimated probability, derived from the observed data, is used to plot the distributions and construct confidence or credibility intervals.
                - The initial input value of p  is **never directly used** in the calculations or visualizations—it serves only as a starting point for generating the simulated data.
                """,
                mathjax=True
            ), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Go to Graphing", href="/graph", color="primary", className="mt-4"), width="auto")
        ]),
    ], fluid=True)




def graphing_page():
    """Layout for the Graphing Page."""
    return dbc.Container([
        # Input Controls
        dbc.Row([
            dbc.Col([
                dbc.Label("Number of Trials (n):"),
                dbc.Input(
                    id="input-n",
                    type="number",
                    value=100,  # Default value
                    min=1,     # Minimum allowed value
                    step=1,
                    className="mb-3"
                ),
                dbc.Label("Probability of Success (p):"),
                dbc.Input(
                    id="input-p",
                    type="number",
                    value=0.5,  # Default value
                    min=0.001,   # Minimum allowed value
                    max=1,      # Maximum allowed value
                    step=0.001,
                    className="mb-3"
                ),
                dbc.Label("Confidence Level:"),
                dcc.Slider(
                    id="input-confidence",
                    min=0.5,
                    max=0.99,
                    step=0.01,
                    value=0.95,
                    marks={0.5: "50%", 0.95: "95%", 0.99: "99%"},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                dbc.Button(
                    "Validate and Generate Graphs",
                    id="generate-button",
                    color="primary",
                    className="mt-3"
                )
            ], width=4),
            dbc.Col([
                html.Div(
                    "Click the button after entering values to generate the probability distributions and intervals.",
                    className="text-muted mt-4"
                )
            ], width=8),
        ], className="mb-4"),

        # Alert for invalid inputs
        dbc.Row([
            dbc.Col([
                dbc.Alert(
                    id="alert",
                    children="",
                    is_open=False,
                    dismissable=True,  # Allow users to dismiss the alert
                )
            ], width=12)
        ]),

        # Graphs
        dbc.Row([
            dbc.Col([
                html.H4("Normal Approximation", className="text-primary"),
                dcc.Loading(
                    id="loading-normal",
                    type="default",
                    children=dcc.Graph(id="plot-normal")
                ),
            ], width=12, className="mb-4"),
            dbc.Col([
                html.H4("Exact Binomial Distribution", className="text-success"),
                dcc.Loading(
                    id="loading-exact",
                    type="default",
                    children=dcc.Graph(id="plot-exact")
                ),
            ], width=12, className="mb-4"),
            dbc.Col([
                html.H4("Bayesian Posterior", className="text-danger"),
                dcc.Loading(
                    id="loading-bayesian",
                    type="default",
                    children=dcc.Graph(id="plot-bayesian")
                ),
            ], width=12),
        ]),
    ], fluid=True)
