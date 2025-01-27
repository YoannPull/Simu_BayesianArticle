from dash import html, dcc
import dash_bootstrap_components as dbc

def create_scenario_section(scenario_name, data):
    """Create a section for a specific scenario."""
    return dbc.Container([
        html.H3(scenario_name, className="text-center text-primary mt-4"),
        html.Div(
            f"n: {data['n']}, p: {data['p']}, Confidence Level: {data['confidence_level']}",
            className="text-muted mb-3",
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=data["normal_plot"]), width=12, className="mb-4"),
            dbc.Col(dcc.Graph(figure=data["exact_plot"]), width=12, className="mb-4"),
            dbc.Col(dcc.Graph(figure=data["bayesian_plot"]), width=12),
        ]),
    ])

def create_layout(precomputed_data):
    """Define the layout with precomputed scenarios."""
    scenarios = [
        create_scenario_section(name, data)
        for name, data in precomputed_data.items()
    ]

    return dbc.Container([
        # Navbar
        dbc.NavbarSimple(
            children=[dbc.NavItem(dbc.NavLink("Home", href="/", id="home-link"))],
            brand="Confidence Interval Comparison",
            brand_href="/",
            color="#404140",
            dark=True,
        ),
        html.Div(id="page-content"),
        *scenarios,  # Add all scenario sections here
    ], fluid=True)
