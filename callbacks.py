from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from utils.plotter import generate_dash_plots
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        """Switch between pages based on the URL."""
        from layout import home_page, graphing_page
        if pathname == "/graph":
            return graphing_page()
        else:
            return home_page()

    @app.callback(
        [
            Output("plot-normal", "figure"),
            Output("plot-exact", "figure"),
            Output("plot-bayesian", "figure"),
            Output("alert", "children"),
            Output("alert", "is_open"),
        ],
        [Input("generate-button", "n_clicks")],
        [State("input-n", "value"), State("input-p", "value"), State("input-confidence", "value")]
    )
    def update_all_plots(n_clicks, n, p, confidence):
        """Generate graphs or show alerts based on user inputs."""
        if not n_clicks:
            raise PreventUpdate

        if n is None or p is None:
            return empty_plot(), empty_plot(), empty_plot(), "Please provide valid values for all inputs.", True

        if n < 1 or p < 0.001:
            return empty_plot(), empty_plot(), empty_plot(), "Values below n=1 or p=0.001 are not allowed.", True

        expected_successes = n * p
        if expected_successes < 1:
            return empty_plot(), empty_plot(), empty_plot(), (
                f"The expected number of successes is too small (n*p={expected_successes:.2f}). "
                "Please increase n or p to generate meaningful results."
            ), True

        fig_normal, fig_exact, fig_bayesian = generate_dash_plots(n, p, confidence)
        return fig_normal, fig_exact, fig_bayesian, "", False


def empty_plot():
    """Generate an empty placeholder plot."""
    fig = go.Figure()
    fig.update_layout(
        title="No Data Available",
        xaxis_title="Proportion",
        yaxis_title="Density",
        template="plotly_white"
    )
    return fig
