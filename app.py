from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import json

# Load precomputed data
with open("precomputed_results.json", "r") as f:
    precomputed_data = json.load(f)

# Function to create layout for each scenario
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

# Create layout with precomputed scenarios
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

# Initialize the Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"]
)

app.title = "Confidence Interval Comparison"

# Set the layout
app.layout = create_layout(precomputed_data)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
