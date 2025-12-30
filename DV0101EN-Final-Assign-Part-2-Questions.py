#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Dataset
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Initialize App
app = dash.Dash(__name__)

# App Layout
year_list = sorted(data["Year"].unique())

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type'
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year'
        )
    ]),

    html.Div(id='output-container', style={'display': 'flex', 'flexDirection': 'column'})
])

# Task 2.4 — Enable/Disable Year Dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return not (selected_statistics == 'Yearly Statistics')

# Task 2.5 — Graph Callback
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):

    # ---------------- Recession Report ----------------
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                     title='Sales During Recession (Yearly Avg)'))

        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R2 = dcc.Graph(figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                                    title='Avg Sales by Vehicle Type During Recession'))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                    title='Ad Expenditure Share During Recession'))

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales',
                                    color='Vehicle_Type', title='Unemployment Rate vs Sales'))

        return [
            html.Div([R1, R2], style={'display': 'flex'}),
            html.Div([R3, R4], style={'display': 'flex'})
        ]

    # ---------------- Yearly Report ----------------
    elif selected_statistics == 'Yearly Statistics' and selected_year is not None:
        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                     title='Yearly Automobile Sales Trend'))

        mas = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                     title=f'Monthly Sales in {selected_year}'))

        avg_v = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y3 = dcc.Graph(figure=px.bar(avg_v, x='Vehicle_Type', y='Automobile_Sales',
                                    title=f'Avg Sales by Vehicle Type ({selected_year})'))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                                    title=f'Ad Expenditure Share ({selected_year})'))

        return [
            html.Div([Y1, Y2], style={'display': 'flex'}),
            html.Div([Y3, Y4], style={'display': 'flex'})
        ]

    return []

# Run App
if __name__ == '__main__':
    app.run(debug=True)
