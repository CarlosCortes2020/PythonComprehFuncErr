import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import re
import os.path
import base64
import io

# Inicializa la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Necesario para desplegar en servidores como Heroku

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Visualizador de Población por País", style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Sección para cargar el archivo
    html.Div([
        html.H3("Paso 1: Cargar archivo CSV"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastra y suelta o ',
                html.A('selecciona un archivo CSV')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload'),
    ]),
    
    # Sección para seleccionar el país
    html.Div([
        html.H3("Paso 2: Seleccionar país"),
        dcc.Dropdown(id='country-dropdown', disabled=True),
        html.Button('Generar Gráfico', id='plot-button', disabled=True, 
                   style={'marginTop': 20, 'padding': '10px', 'backgroundColor': '#4CAF50', 'color': 'white'}),
    ], style={'marginTop': 30}),
    
    # Sección para mostrar la gráfica
    html.Div([
        html.H3("Gráfico de Población", id='graph-title', style={'display': 'none'}),
        dcc.Graph(id='population-graph'),
    ], style={'marginTop': 30}),
    
    # Almacenamiento de datos
    dcc.Store(id='stored-data'),
    dcc.Store(id='country-column'),
    dcc.Store(id='year-columns'),
    
    # Pie de página
    html.Footer([
        html.Hr(),
        html.P("Visualizador de Población - Creado con Dash", style={'textAlign': 'center'})
    ], style={'marginTop': 50})
])

def parse_contents(contents, filename):
    """
    Procesa el contenido del archivo cargado
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename.lower():
            # Leer el archivo CSV
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            # Identificar columnas de países y años
            country_column = find_country_column(df)
            year_columns = find_year_columns(df)
            
            if country_column and year_columns:
                return html.Div([
                    html.H5(f"Archivo cargado: {filename}"),
                    html.P(f"Contiene {df.shape[0]} filas y {df.shape[1]} columnas."),
                    html.P(f"Columna de países identificada: {country_column}"),
                    html.P(f"Años identificados: {', '.join(year_columns[:5])}{'...' if len(year_columns) > 5 else ''}")
                ]), df.to_json(date_format='iso', orient='split'), country_column, year_columns
            else:
                return html.Div([
                    html.H5(f"Archivo cargado: {filename}"),
                    html.P("No se pudieron identificar las columnas necesarias en el archivo.")
                ]), None, None, None
        else:
            return html.Div([
                html.H5(f"El archivo {filename} no es un CSV válido.")
            ]), None, None, None
    except Exception as e:
        return html.Div([
            html.H5(f"Error al procesar el archivo: {filename}"),
            html.P(str(e))
        ]), None, None, None

def find_country_column(df):
    """
    Encuentra la columna que contiene los nombres de países en el DataFrame.
    """
    # Primero intenta buscar columnas con palabras clave que indiquen países
    for column in df.columns:
        if re.search(r'country|pais|país', column.lower()):
            return column
    
    # Intenta un enfoque alternativo: buscar columnas que contengan texto (objetos)
    text_columns = df.select_dtypes(include=['object']).columns
    
    if len(text_columns) > 0:
        return text_columns[0]
    
    return None


def find_year_columns(df):
    """
    Encuentra las columnas que representan años en los encabezados del DataFrame.
    """
    year_columns = []
    
    for column in df.columns:
        if re.match(r'^\d{4}', str(column)):
            year_columns.append(column)
    
    # Ordena las columnas de años numéricamente
    year_columns.sort(key=lambda x: int(re.match(r'^\d{4}', x).group()))
    
    return year_columns


@app.callback(
    [Output('output-data-upload', 'children'),
     Output('stored-data', 'data'),
     Output('country-column', 'data'),
     Output('year-columns', 'data'),
     Output('country-dropdown', 'options'),
     Output('country-dropdown', 'disabled'),
     Output('plot-button', 'disabled')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        return None, None, None, None, [], True, True
    
    children, data, country_column, year_columns = parse_contents(contents, filename)
    
    if data is None:
        return children, None, None, None, [], True, True
    
    # Cargar DataFrame desde los datos almacenados
    df = pd.read_json(data, orient='split')
    
    # Crear opciones para el dropdown de países
    country_options = [{'label': country, 'value': country} 
                      for country in sorted(df[country_column].unique())]
    
    return children, data, country_column, year_columns, country_options, False, False


@app.callback(
    [Output('population-graph', 'figure'),
     Output('graph-title', 'style')],
    [Input('plot-button', 'n_clicks')],
    [State('stored-data', 'data'),
     State('country-column', 'data'),
     State('year-columns', 'data'),
     State('country-dropdown', 'value')]
)
def update_graph(n_clicks, data, country_column, year_columns, selected_country):
    if n_clicks is None or data is None or selected_country is None:
        return {}, {'display': 'none'}
    
    # Cargar DataFrame desde los datos almacenados
    df = pd.read_json(data, orient='split')
    
    # Filtrar datos para el país seleccionado
    country_data = df[df[country_column] == selected_country]
    
    if country_data.empty:
        return {}, {'display': 'none'}
    
    # Diccionario para almacenar los datos de población por año
    population_data = {}
    
    # Recorre cada columna de año para extraer los valores de población
    for year in year_columns:
        try:
            year_str = str(year)
            
            if not country_data[year_str].empty:
                population = country_data[year_str].iloc[0]
                
                try:
                    population = float(population)
                    # Extrae solo el año (primeros 4 dígitos) para la visualización
                    year_display = year_str[:4]
                    population_data[year_display] = population
                except (ValueError, TypeError):
                    pass
        except KeyError:
            continue
    
    # Crear DataFrame para Plotly
    plot_df = pd.DataFrame({
        'Año': list(population_data.keys()),
        'Población': list(population_data.values())
    })
    
    # Crear gráfico con Plotly Express
    fig = px.line(
        plot_df, 
        x='Año', 
        y='Población', 
        title=f'Población de {selected_country} por Año',
        markers=True
    )
    
    # Personalizar el diseño del gráfico
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        xaxis_tickangle=45,
        yaxis=dict(
            tickformat=',',
        ),
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig, {'display': 'block'}


if __name__ == '__main__':
    app.run_server(debug=True)