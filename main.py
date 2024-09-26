from flask import Flask
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html

# Load the Excel file to inspect its contents
file_path = "data/DATA.xlsx"
xls = pd.ExcelFile(file_path)

# Check sheet names to identify relevant data
xls.sheet_names

# Load the data from the 'DATA' sheet to explore its structure and contents
data_df = pd.read_excel(file_path, sheet_name="DATA")

# Now let's load the 'Description' sheet to understand the meaning of each column
description_df = pd.read_excel(file_path, sheet_name="Description")

# Create a Flask app
flask_app = Flask(__name__)

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
]

# Create a Dash app for the dashboard
dash_app = Dash(
    __name__,
    server=flask_app,
    url_base_pathname="/dashboard/",
    external_stylesheets=external_stylesheets,
)


# 1 . Loan Amount Distribution
data_df["Amount_issued"] = pd.to_numeric(data_df["Amount_issued"], errors="coerce")

# Create a histogram with Plotly Express
fig1 = px.histogram(
    data_df, x="Amount_issued", nbins=30, title="Distribution of Loan Amounts"
)

# Customize axis labels and layout
fig1.update_layout(
    xaxis_title="Loan Amount",
    yaxis_title="Frequency",
    bargap=0.1,  # Adjusts the gap between bars
)

fig2 = px.histogram(
    data_df,
    x="Baking_Loan_delinquency",
    nbins=30,
    title="Distribution of Loan Delinquency",
    color_discrete_sequence=["green"],
)
fig2.update_layout(xaxis_title="Delinquency Value", yaxis_title="Frequency", bargap=0.1)


# 3. Loan Terms Distribution
fig3 = px.histogram(
    data_df,
    x="Term",
    nbins=20,
    title="Distribution of Loan Terms",
    color_discrete_sequence=["orange"],
)
fig3.update_layout(xaxis_title="Loan Term (Days)", yaxis_title="Frequency")


# 4. Fraud Score Analysis
fig4 = px.histogram(
    data_df,
    x="AntiFraud_score",
    nbins=20,
    title="Distribution of Anti-Fraud Scores",
    color_discrete_sequence=["#F5004F"],
)
fig4.update_layout(xaxis_title="Anti-Fraud Score", yaxis_title="Frequency")

# 5. Distribution of Client Accounts
fig5 = px.histogram(
    data_df,
    x="Accounts",
    nbins=20,
    title="Distribution of Client Accounts",
    color_discrete_sequence=["purple"],
)
fig5.update_layout(xaxis_title="Number of Accounts", yaxis_title="Frequency")


# 6. Analysis of Entity Types
fig6 = px.histogram(
    data_df,
    x="Real_TipoEntidad_AFIS",
    nbins=15,
    title="Distribution of Entity Types (AFIS)",
    color_discrete_sequence=["cyan"],
)
fig6.update_layout(xaxis_title="Entity Type (AFIS)", yaxis_title="Frequency")


# 7. Baking Loan at Day - how much of the loan was active at a specific day
fig7 = px.histogram(
    data_df,
    x="Baking_Loan_at_day",
    nbins=20,
    title="Distribution of Baking Loan at Day",
    color_discrete_sequence=["magenta"],
)
fig7.update_layout(xaxis_title="Baking Loan at Day", yaxis_title="Frequency")


# 8. Loan Close-Out Distribution
data_df["Baking_Loan_Close"] = pd.to_numeric(
    data_df["Baking_Loan_Close"], errors="coerce"
)

fig8 = px.histogram(
    data_df,
    x="Baking_Loan_Close",
    nbins=20,
    title="Distribution of Loan Close-Out Values",
    color_discrete_sequence=["brown"],
)
fig8.update_layout(xaxis_title="Loan Close-Out Value", yaxis_title="Frequency")

# 9. Total Outstanding Balance Across All Accounts
data_df["TotalSaldoTotal_2"] = pd.to_numeric(
    data_df["TotalSaldoTotal_2"], errors="coerce"
)

fig9 = px.histogram(
    data_df,
    x="TotalSaldoTotal_2",
    nbins=20,
    title="Distribution of Total Outstanding Balances",
    color_discrete_sequence=["teal"],
)
fig9.update_layout(xaxis_title="Total Outstanding Balance", yaxis_title="Frequency")

# 10. Overdue Amounts Across Loans (ValorMora_2)
data_df["ValorMora_2"] = pd.to_numeric(data_df["ValorMora_2"], errors="coerce")

fig10 = px.histogram(
    data_df,
    x="ValorMora_2",
    nbins=20,
    title="Distribution of Overdue Loan Amounts (Valor Mora)",
    color_discrete_sequence=["darkgreen"],
)
fig10.update_layout(xaxis_title="Overdue Amount", yaxis_title="Frequency")

# 11. Age Range Analysis
age_range_counts = data_df["RangoEdad"].value_counts().sort_index()

fig11 = px.bar(
    age_range_counts,
    x=age_range_counts.index,
    y=age_range_counts.values,
    title="Distribution of Loan Issuances by Age Range",
    labels={"x": "Age Range", "y": "Number of Loans"},
    color_discrete_sequence=["skyblue"],
)

fig11.update_layout(xaxis_tickangle=-45)

dash_app.layout = html.Div(
    children=[
        html.H1(
            children="Análisis exploratorio y descriptivo (EDA)",
            style={
                "fontSize": "3rem",
                "fontFamily": "'Montserrat', serif",
                "color": "#373A40",
                "marginLeft": "25px",
            },
        ),
        html.Div(
            children="""Visualización de la base de datos de la información crediticia.""",
            style={
                "fontSize": "1rem",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "25px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="amount-issued-bar", figure=fig1),
        html.P(
            children="""Como se puede ver, el monto más común de préstamos está entre $200.000 y $240.000.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Baking_Loan_delinquency", figure=fig2),
        html.P(
            children="""Alrededor del 95% de los clientes tienen cero obligaciones en mora.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Term", figure=fig3),
        html.P(
            children="""La duración de los préstamos, frecuentemete, es de 30 días, seguido por 20 días""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="AntiFraud_score", figure=fig4),
        html.P(
            children="""Para este indicador se observan valores bajos, menores a 1. Lo que indica que la acción es segura y se aprobará en la mayoría de los casos.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Accounts", figure=fig5),
        html.P(
            children="""La mayoría de los clientes tienen entre 1 y 4 cuentas bancarias, pero también un gran porcentaje tienen 5 o más.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Real_TipoEntidad_AFIS", figure=fig6),
        html.P(
            children="""La cantidad de obligaciones por tipo de entidad está entre 0 y 4.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Baking_Loan_at_day", figure=fig7),
        html.P(
            children="""Gran parte de los clientes tiene sus obligacion al día, ya que más del 90% de los clientes tienen entre 0 y 4.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="Baking_Loan_Close", figure=fig8),
        html.P(
            children="""Más de 11.000 clientes tienen saldadas hasta 50 obligaciones""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="TotalSaldoTotal_2", figure=fig9),
        html.P(
            children="""La deuda total no supera los $40.000.000 en la gran mayoría""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="ValorMora_2", figure=fig10),
        html.P(
            children="""El saldo reportado en mora no supera los $500.000, en un gran porcentaje.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
        dcc.Graph(id="distribution-of-loan-issuances-by-age-range", figure=fig11),
        html.P(
            children="""Se puede ver que la gente entre 31 y 35 años es más propensa a realizar préstamos. 
            Incluso, personas más jóvenes entre 18 y 30 años tienen un porcentaje alto. Este porcentaje decae para personas mayores de 55 años.""",
            style={
                "fontSize": "14px",
                "color": "#373A40",
                "fontFamily": "'Montserrat', serif",
                "marginLeft": "35px",
                "fontWeight": "500",
            },
        ),
    ]
)


# Flask route for the main page
@flask_app.route("/")
def home():
    return "Dashboard"


# Run the Flask app
if __name__ == "__main__":
    flask_app.run(port=8080)
