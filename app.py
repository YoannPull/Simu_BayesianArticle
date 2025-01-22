from dash import Dash
from layout import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"]
)

app.title = "Confidence Interval Comparison"

# Set the layout
app.layout = create_layout()

# Register the callbacks
register_callbacks(app)

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
