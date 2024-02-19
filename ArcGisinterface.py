import arcgis
import pandas as pd
import pyodbc
from ipywidgets import interact, widgets

# Connect to GIS Enterprise portal
gis = arcgis.gis.GIS("https://myportal.com/portal", "myusername", "mypassword")

# Connect to SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver.com;DATABASE=mydatabase;UID=myusername;PWD=mypassword')

# Query data from SQL Server
def query_data(table_name):
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, conn)
    return data

# Create a new feature layer from the data
def create_feature_layer(data):
    feature_layer = gis.content.create("Feature Layer", data)
    return feature_layer

# Visualize the feature layer on a map
def visualize_feature_layer(feature_layer):
    map = gis.map("My Map", feature_layer)
    return map

# Manipulate the data by adding a new field
def add_new_field(feature_layer, field_name, field_value):
    with arcgis.features.FeatureLayer(feature_layer.url) as fl:
        fl.edit_features(adds={field_name: field_value})
    feature_layer.save()

# Disconnect from the SQL Server
def disconnect_sql_server():
    conn.close()

# User interface
def user_interface():
    table_name = widgets.Text(description='Table Name:')
    field_name = widgets.Text(description='Field Name:')
    field_value = widgets.Text(description='Field Value:')
    
    def on_click(button):
        data = query_data(table_name.value)
        feature_layer = create_feature_layer(data)
        map = visualize_feature_layer(feature_layer)
        add_new_field(feature_layer, field_name.value, field_value.value)
        disconnect_sql_server()
        
    button = widgets.Button(description='Visualize and Manipulate Data')
    button.on_click(on_click)
    
    display(table_name, field_name, field_value, button)

user_interface()