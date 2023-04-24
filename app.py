import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd

from dash import dash_table

# df = pd.read_csv('assets/data/gapminderDataFiveYear.csv')

dash_app = dash.Dash(__name__)
app = dash_app.server

df = pd.read_csv('Hi.csv', header=0)

dash_app.layout = html.Div([
    dash_table.DataTable(
        id='computed-table',
        columns=[
            {'name': 'name', 'id': 'input-data-1'},
            {'name': 'age', 'id': 'input-data-2'}
        ],
        data=[{'input-data-1': df.iloc[i]['Name'], 'input-data-2': df.iloc[i]['Age']} for i in range(df.shape[0])],
        editable=True,
    ),
])


@dash_app.callback(
    Output('computed-table', 'data'),
    Input('computed-table', 'data_timestamp'),
    State('computed-table', 'data'))
def update_columns(timestamp, rows):
    Name = []
    Age = []
    i = 0
    for row in rows:
        try:
            Name.append(row['input-data-1'])
            Age.append(row['input-data-2'])
        except:
            print('Error')
    df_temp = pd.DataFrame(data={'Name': Name, 'Age': Age})
    df_temp.to_csv('Hi.csv')
    return rows


if __name__ == '__main__':
    dash_app.run_server(debug=True)
