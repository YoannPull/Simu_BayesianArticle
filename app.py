from dash import Dash, html, dcc, Input, Output, State, ALL, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import os

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Helper functions
def create_home_page():
    """Creates the welcome page."""
    return dbc.Container(
        [
            dbc.NavbarSimple(
                brand="Confidence Interval Comparison",
                brand_href="/",
                children=[
                    dbc.NavLink("Home", href="/", className="text-white"),
                ],
                color="#bd8e43",
                dark=True,
            ),
            html.Div(
                [
                    html.H1("Welcome to Confidence Interval Comparison App", className="text-center my-4"),
                    html.P(
                        "This app showcases precomputed confidence intervals using different statistical methods "
                        "for various scenarios. You can click on any graphic to view it in a larger scale.",
                        className="text-center text-dark mb-4 fw-bold",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Markdown(
                                    r"""
                                    This application provides a platform to explore and compare confidence and credibility intervals using simulated data.

                                    ### How It Works
                                    - The parameters \(n\) (number of trials) and \(p\) (probability of success) are used to generate observations following a Bernoulli process (1 for success, 0 for failure).
                                    - In real-world scenarios, these observations would come from actual experiments or data collection.
                                    - A commonly used method to estimate the theoretical probability of success is:
                                      $$
                                      \hat{p} = \frac{\sum Y_i}{n}
                                      $$
                                      where \(Y_i\) represents individual Bernoulli trials.

                                    ### Key Details
                                    - The estimated probability, derived from the observed data, is used to plot the distributions and construct confidence or credibility intervals.
                                    - The initial input value of \(p\) is **never directly used** in the calculations or visualizations—it serves only as a starting point for generating the simulated data.
                                    """,
                                    mathjax=True,
                                ),
                                width=12,
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Baseline Scenarios",
                                    href="/baseline",
                                    color="primary",
                                    className="btn-block my-2",
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Low Default Portfolio Scenarios",
                                    href="/low-default",
                                    color="primary",
                                    className="btn-block my-2",
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Large Sample Scenarios",
                                    href="/large-sample",
                                    color="primary",
                                    className="btn-block my-2",
                                ),
                                width=4,
                            ),
                        ],
                        className="justify-content-center mt-4",
                    ),
                ],
                className="mt-4",
            ),
        ],
        fluid=True,
    )


def create_scenario_window(title, image_dir, keyword):
    """Creates a layout for a specific scenario category."""
    scenario_cards = []
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpeg") and keyword in image_file.lower():
            scenario_name = image_file.replace("_", " ").replace(".jpeg", "").title()
            image_path = f"/{image_dir}/{image_file}"
            scenario_cards.append(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(scenario_name, className="card-title"),
                                html.Img(
                                    src=image_path,
                                    className="img-fluid",
                                    style={"maxHeight": "200px", "cursor": "pointer"},
                                    id={"type": "image", "index": image_file},
                                ),
                            ]
                        ),
                        className="mb-4",
                    ),
                    width=4,
                )
            )

    return dbc.Container(
        [
            dbc.NavbarSimple(
                brand=title,
                children=[
                    dbc.NavLink("Back to Home", href="/", className="text-white"),
                ],
                color="#bd8e43",
                dark=True,
            ),
            html.Div(
                [
                    html.P(
                        "Remember to click on the graphic to view it in a higher scale.",
                        className="text-center text-dark mb-4 fw-bold",
                        style={"color": "#404140"},
                    ),
                    dbc.Row(scenario_cards, className="g-4"),
                ],
                className="mb-4",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                    dbc.ModalBody(html.Img(id="modal-image", className="img-fluid")),
                ],
                id="modal",
                is_open=False,
                size="lg",
            ),
        ],
        fluid=True,
    )


# Define the app layout
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ]
)


# Callbacks
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    """Switches between pages."""
    if pathname == "/baseline":
        return create_scenario_window("Baseline Scenarios", "assets/plots", "baseline")
    elif pathname == "/low-default":
        return create_scenario_window("Low Default Portfolio Scenarios", "assets/plots", "low default")
    elif pathname == "/large-sample":
        return create_scenario_window("Large Sample Scenarios", "assets/plots", "large sample")
    else:
        return create_home_page()


@app.callback(
    [Output("modal", "is_open"), Output("modal-title", "children"), Output("modal-image", "src")],
    [Input({"type": "image", "index": ALL}, "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n_clicks, is_open):
    """Toggles the modal for displaying enlarged images."""
    if not any(n_clicks):
        raise PreventUpdate

    triggered_id = ctx.triggered_id
    if triggered_id:
        image_file = triggered_id["index"]
        image_name = image_file.replace("_", " ").replace(".jpeg", "").title()
        image_path = f"/assets/plots/{image_file}"
        return not is_open, image_name, image_path
    return is_open, None, None


# Run the app
if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port=8050, debug=True)
