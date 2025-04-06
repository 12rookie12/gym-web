
from flask import Flask,render_template
import dash
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
from database import add_data, fetch_data

server = Flask(__name__)  # ✅ Define the Flask server

# Initialize Dash App
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/")

# Function to fetch data from database
def get_dataframe():
    data = fetch_data()
    return (
        pd.DataFrame(data, columns=["Date", "Calories_Intake", "Calories_Burned"])
        if data
        else pd.DataFrame()
    )

# Layout
app.layout = html.Div(
    style={"backgroundColor": "#1e1e1e", "color": "white", "padding": "20px"},
    children=[
        html.H1("🔥 Calories Burned vs. Food Intake", style={"textAlign": "center"}),
        # Graphs
        html.Div(
            [
                dcc.Graph(id="calories-comparison-graph"),
                dcc.Graph(id="calorie-pie-chart"),
            ],
            style={"display": "flex", "flexDirection": "row"},
        ),
        # User Input
        html.Div(
            [
                html.Label("Date:", style={"marginTop": "10px"}),
                dcc.DatePickerSingle(
                    id="date-input", date="2025-03-20", display_format="YYYY-MM-DD"
                ),
                html.Label("Calories Intake:", style={"marginTop": "10px"}),
                dcc.Input(id="calories-intake", type="number", value=2000, step=50),
                html.Label("Calories Burned:", style={"marginTop": "10px"}),
                dcc.Input(id="calories-burned", type="number", value=2200, step=50),
                html.Button(
                    "Add Data",
                    id="add-btn",
                    n_clicks=0,
                    style={
                        "marginTop": "20px",
                        "padding": "10px 20px",
                        "backgroundColor": "#FF5733",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "maxWidth": "400px",
                "margin": "auto",
            },
        ),
        # Weight Prediction Section
        html.Div(
            [
                html.H3("📊 Predicted Weight Change:", style={"textAlign": "center"}),
                html.H2(
                    id="weight-prediction",
                    style={"textAlign": "center", "color": "#FF5733"},
                ),
            ]
        ),
    ],
)

# Callback to Update Graphs & Predict Weight
@app.callback(
    [Output("calorie-pie-chart", "figure"), Output("calories-comparison-graph", "figure"), Output("weight-prediction", "children")],
    [Input("add-btn", "n_clicks")],
    [State("date-input", "date"), State("calories-intake", "value"), State("calories-burned", "value")],
)
def update_graph(n_clicks, date, intake, burned):
    if n_clicks > 0:
        add_data(date, intake, burned)

    df = get_dataframe()
    if df.empty:
        return go.Figure(), go.Figure(), "No Data"

    # Line Chart: Calories Burned vs. Consumed
    fig1 = px.line(
        df,
        x="Date",
        y=["Calories_Intake", "Calories_Burned"],
        labels={"value": "Calories", "variable": "Type"},
        title="📈 Calories Consumed vs. Burned Over Time",
        markers=True,
        template="plotly_dark",
    )

    # Pie Chart: Calories Intake Distribution
    avg_intake = df["Calories_Intake"].mean()
    avg_burned = df["Calories_Burned"].mean()

    fig2 = go.Figure(
        data=[
            go.Pie(
                labels=["Calories Intake", "Calories Burned"],
                values=[avg_intake, avg_burned],
                hole=0.4,
                marker=dict(colors=["#ff6361", "#58508d"]),
            )
        ]
    )
    fig2.update_layout(
        title_text="🍽️ Calories Intake vs. Burned Distribution", template="plotly_dark"
    )

    # Weight Prediction Model
    df["Calorie_Difference"] = df["Calories_Intake"] - df["Calories_Burned"]

    # Use the latest caloric difference (last recorded entry)
    if not df.empty:
        latest_diff = df["Calorie_Difference"].iloc[-1]  # Get last caloric difference
        
        # Weight gain/loss formula: ~7700 calories = 1kg
        weight_change = round(latest_diff / 7700, 2)
    else:
        weight_change = 0

    return fig2, fig1, f"Predicted Weight Change: {weight_change} kg"

@server.route("/track")
def track():
    return render_template("progress.html") 

# Run App
if __name__ == "__main__":
    app.run(debug=True)  # ✅ NEW (Works)
