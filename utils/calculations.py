from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "Confidence Interval Comparison"

# Helper function to create a card for each scenario
def create_scenario_card(scenario_name, image_path):
    """Create a card for a scenario with its image."""
    return dbc.Card(
        dbc.CardBody([
            html.H5(scenario_name, className="card-title text-center"),
            html.Img(
                src=image_path,
                className="img-fluid scenario-image",
                style={"cursor": "pointer"},
                id=f"image-{scenario_name.replace(' ', '-')}",
            ),
        ]),
        className="mb-4",
    )

# Layout for each section (Baseline, Low Default, Large Sample)
def create_scenario_section(title, scenario_cards):
    return html.Div([
        html.H2(title, className="text-center my-4 text-primary"),
        dbc.Row(
            [dbc.Col(card, width=4) for card in scenario_cards],
            className="g-4",
        ),
    ], className="mt-4")

# Main Layout
def create_layout():
    # Read image files
    image_dir = "assets/plots"
    baseline_cards = []
    low_default_cards = []
    large_sample_cards = []

    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpeg"):
            scenario_name = image_file.replace("_", " ").replace(".jpeg", "").title()
            image_path = f"/{image_dir}/{image_file}"

            if "Baseline" in scenario_name:
                baseline_cards.append(create_scenario_card(scenario_name, image_path))
            elif "Low Default" in scenario_name:
                low_default_cards.append(create_scenario_card(scenario_name, image_path))
            elif "Large Sample" in scenario_name:
                large_sample_cards.append(create_scenario_card(scenario_name, image_path))

    return dbc.Container(
        [
            # Navbar
            dbc.NavbarSimple(
                brand="Confidence Interval Comparison",
                brand_href="/",
                color="primary",
                dark=True,
            ),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
        ],
        fluid=True,
    )

# Welcome Page Layout
def welcome_page():
    return dbc.Container(
        [
            html.H1("Welcome to the Confidence Interval Comparison Tool", className="text-center my-4"),
            html.P("Navigate through different scenarios to visualize confidence intervals.", className="text-center"),
            dbc.Button("Explore Scenarios", href="/scenarios", color="primary", size="lg", className="d-block mx-auto"),
        ],
        fluid=True,
        className="mt-5",
    )

# Scenarios Page Layout
def scenarios_page():
    image_dir = "assets/plots"
    baseline_cards = []
    low_default_cards = []
    large_sample_cards = []

    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpeg"):
            scenario_name = image_file.replace("_", " ").replace(".jpeg", "").title()
            image_path = f"/{image_dir}/{image_file}"

            if "Baseline" in scenario_name:
                baseline_cards.append(create_scenario_card(scenario_name, image_path))
            elif "Low Default" in scenario_name:
                low_default_cards.append(create_scenario_card(scenario_name, image_path))
            elif "Large Sample" in scenario_name:
                large_sample_cards.append(create_scenario_card(scenario_name, image_path))

    return dbc.Container(
        [
            create_scenario_section("Baseline Scenarios", baseline_cards),
            create_scenario_section("Low Default Portfolio Scenarios", low_default_cards),
            create_scenario_section("Large Sample Scenarios", large_sample_cards),
            # Modal for larger image
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                    dbc.ModalBody(html.Img(id="modal-image", className="img-fluid")),
                ],
                id="image-modal",
                size="lg",
            ),
        ],
        fluid=True,
    )

# App Layout
app.layout = create_layout()

# Callback for page navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/scenarios":
        return scenarios_page()
    return welcome_page()

# Callback for opening the modal
@app.callback(
    [Output("modal-title", "children"), Output("modal-image", "src"), Output("image-modal", "is_open")],
    [Input({"type": "image", "index": ALL}, "n_clicks")],
    [State({"type": "image", "index": ALL}, "id")],
    prevent_initial_call=True,
)
def open_image_modal(n_clicks, ids):
    ctx = dash.callback
