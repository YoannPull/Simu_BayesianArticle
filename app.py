import os
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


if __name__ == "__main__":
    # Render fournit le port dans la variable d'environnement `PORT`
    port = int(os.environ.get("PORT", 8050))  # Par défaut 8050 si non spécifié
    app.run_server(host="0.0.0.0", port=port)

