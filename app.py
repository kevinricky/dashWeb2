import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd
import csv
import os
import time

from dash import dash_table

from azure.storage.blob import BlobServiceClient

# df = pd.read_csv('assets/data/gapminderDataFiveYear.csv')

dash_app = dash.Dash(__name__)
app = dash_app.server

# df = pd.read_csv('Hi.csv', header=0)
connect_str = 'DefaultEndpointsProtocol=https;AccountName=dashstorageforkevin;AccountKey=A5qu9+GmBBhdwC3oz2s3ADYFMOaP4P7kQoWtuw9rDa533BFTDqGgy6XvEUcj2yeItBC9MPgZXTxB+AStsT4eXQ==;EndpointSuffix=core.windows.net'
bsc = BlobServiceClient.from_connection_string(connect_str)
blob_client_instance = bsc.get_blob_client('dashcontainersample', 'Hi.csv', snapshot=None)
if not os.path.exists("tmp"):
    os.mkdir('tmp')
with open('tmp/Temp_Hi.csv', "wb") as my_blob:
    blob_data = blob_client_instance.download_blob()
    blob_data.readinto(my_blob)
df = pd.read_csv('tmp/Temp_Hi.csv')

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


def writeDataToBlob(df_temp):
    # Create a blob client using the local file name as the name for the blob
    bsc = BlobServiceClient.from_connection_string(connect_str)
    cc = bsc.get_container_client('dashcontainersample')
    print('Writing data')

    fn = 'tmp/Hi.csv'
    with open(fn, mode='w', newline='') as cf:
        writer = csv.writer(cf)
        writer.writerow(df_temp.columns.tolist())
        for i in range(df_temp.shape[0]):
            writer.writerow(df_temp.loc[i, :].values.tolist())
    print('Write data into container')
    bc = bsc.get_blob_client('dashcontainersample', 'Hi.csv', snapshot=None)
    with open(fn, 'rb') as data:
        # bc.rename_blob('Hi_'+str(time.time()+'.csv'))
        bc.delete_blob()
        bc.upload_blob(data)
    return


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
    # df_temp.to_csv('Hi.csv')
    writeDataToBlob(df_temp)
    return rows


if __name__ == '__main__':
    dash_app.run_server(debug=True)
