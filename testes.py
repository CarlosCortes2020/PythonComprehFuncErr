import pandas as pd  # Importa la biblioteca pandas para manipulación y análisis de datos
import matplotlib.pyplot as plt  # Importa pyplot de matplotlib para crear gráficos y visualizaciones
import re  # Importa el módulo de expresiones regulares para buscar patrones en texto
import os.path  # Importa funciones para trabajar con rutas de archivos
import sys  # Importa funciones del sistema, aunque no se usa directamente en este código


def load_csv_file(file_path):
    """
    Carga un archivo CSV y lo devuelve como un DataFrame de pandas.
    
    Args:
        file_path (str): Ruta al archivo CSV
    
    Returns:
        pandas.DataFrame: DataFrame con los datos cargados, None si hay error
    """
    try:
        # Intenta cargar el archivo CSV utilizando la función read_csv de pandas
        # Esta función lee el contenido del archivo y lo convierte en un DataFrame
        df = pd.read_csv(file_path)
        return df  # Devuelve el DataFrame si la carga fue exitosa
    except Exception as e:
        # Captura cualquier error que pueda ocurrir durante la carga (archivo inexistente, mal formateado, etc.)
        print(f"Error al cargar el archivo CSV: {e}")  # Muestra el mensaje de error
        return None  # Devuelve None para indicar que hubo un problema


def find_country_column(df):
    """
    Encuentra la columna que contiene los nombres de países en el DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos
    
    Returns:
        str or None: Nombre de la columna de países o None si no se encuentra
    """
    # Primero intenta buscar columnas con palabras clave que indiquen países
    for column in df.columns:  # Itera por cada nombre de columna en el DataFrame
        # Usa expresiones regulares para buscar palabras relacionadas con países
        if re.search(r'country|pais|país', column.lower()):
            return column  # Si encuentra una coincidencia, devuelve el nombre de esa columna
    
    # Si no se encuentra una columna con nombre explícito de país, muestra mensajes informativos
    print("No se encontró una columna explícita de países.")
    print("Intentando identificar la columna por el tipo de datos...")
    
    # Intenta un enfoque alternativo: buscar columnas que contengan texto (objetos)
    # select_dtypes filtra las columnas por tipo de datos
    text_columns = df.select_dtypes(include=['object']).columns
    
    if len(text_columns) > 0:  # Si hay al menos una columna de texto
        # Asume que la primera columna de texto podría contener nombres de países
        print(f"Usando la columna '{text_columns[0]}' como posible columna de países.")
        return text_columns[0]  # Devuelve el nombre de esta columna
    
    # Si no se encuentra ninguna columna adecuada, devuelve None
    return None


def find_year_columns(df):
    """
    Encuentra las columnas que representan años en los encabezados del DataFrame.
    Busca columnas cuyo nombre comience con 4 dígitos (como "2022 Population").
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos
    
    Returns:
        list: Lista ordenada de nombres de columnas que contienen años
    """
    year_columns = []  # Inicializa una lista vacía para almacenar los nombres de columnas
    
    # Recorre cada columna del DataFrame
    for column in df.columns:
        # Verifica si el nombre de la columna comienza con 4 dígitos (un año)
        # ^ indica inicio de cadena, \d{4} significa exactamente 4 dígitos
        if re.match(r'^\d{4}', str(column)):
            year_columns.append(column)  # Si coincide, agrega el nombre a la lista
    
    # Ordena las columnas de años numéricamente 
    # La función lambda extrae los primeros 4 dígitos y los convierte a entero
    year_columns.sort(key=lambda x: int(re.match(r'^\d{4}', x).group()))
    
    return year_columns  # Devuelve la lista ordenada de columnas


def plot_country_population(df, country_column, year_columns, country_name):
    """
    Genera un gráfico de la población de un país específico a lo largo del tiempo.
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos
        country_column (str): Nombre de la columna que contiene los países
        year_columns (list): Lista de columnas que representan años
        country_name (str): Nombre del país a graficar
    
    Returns:
        bool: True si se generó el gráfico correctamente, False en caso contrario
    """
    # Filtra el DataFrame para obtener solo las filas del país especificado
    # Crea un nuevo DataFrame que solo contiene datos del país seleccionado
    country_data = df[df[country_column] == country_name]
    
    # Verifica si se encontraron datos para ese país
    if country_data.empty:
        print(f"No se encontraron datos para {country_name}")
        return False  # Devuelve False si no hay datos
    
    # Diccionario para almacenar los datos de población por año
    population_data = {}
    
    # Recorre cada columna de año para extraer los valores de población
    for year in year_columns:
        try:
            # Convierte el nombre de la columna a string por si acaso no lo es
            year_str = str(year)
            
            # Verifica que existan valores para este año
            if not country_data[year_str].empty:
                # Obtiene el primer valor de población para este año y país
                # iloc[0] accede al primer elemento de la serie
                population = country_data[year_str].iloc[0]
                
                # Intenta convertir el valor a número flotante
                # Algunos valores podrían ser strings o tener formato no numérico
                try:
                    population = float(population)
                    # Almacena el par año-población en el diccionario
                    population_data[year_str] = population
                except (ValueError, TypeError):
                    # Si no se puede convertir a número, ignora este año
                    pass
        except KeyError:
            # Si la columna no existe en el DataFrame, continúa con la siguiente
            continue
    
    # Verifica si se encontraron datos de población válidos
    if not population_data:
        print(f"No hay datos de población para {country_name}")
        return False  # Devuelve False si no hay datos válidos
    
    # Comienza la creación del gráfico
    # Crea una nueva figura con tamaño 12x6 pulgadas
    plt.figure(figsize=(12, 6))
    
    # Dibuja la línea del gráfico con los datos de población
    # Usa los años como eje X y los valores de población como eje Y
    # marker='o' añade puntos en cada dato, linestyle='-' conecta los puntos con líneas
    plt.plot(list(population_data.keys()), list(population_data.values()), marker='o', linestyle='-', color='blue')
    
    # Configura el título del gráfico con el nombre del país, tamaño de fuente 16
    plt.title(f'Población de {country_name} por Año', fontsize=16)
    
    # Etiqueta para el eje X (años), tamaño de fuente 12
    plt.xlabel('Año', fontsize=12)
    
    # Etiqueta para el eje Y (población), tamaño de fuente 12
    plt.ylabel('Población', fontsize=12)
    
    # Agrega una cuadrícula al gráfico para facilitar la lectura
    # linestyle='--' crea líneas punteadas, alpha=0.7 las hace semitransparentes
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rota las etiquetas del eje X 45 grados para mejor legibilidad
    plt.xticks(rotation=45)
    
    # Formatea los números del eje Y con separadores de miles
    # Convierte cada valor a entero y luego a string con formato "{:,}"
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Ajusta automáticamente los márgenes y espaciado del gráfico
    plt.tight_layout()
    
    # Muestra el gráfico en pantalla
    plt.show()
    
    # Devuelve True para indicar que el gráfico se generó correctamente
    return True


def main():
    """
    Función principal que coordina la ejecución del programa.
    Solicita al usuario la ruta del archivo, carga los datos y permite
    seleccionar países para visualizar su población.
    """
    # Solicita al usuario que ingrese la ruta del archivo CSV
    # strip() elimina espacios en blanco al inicio y final
    file_path = input("Ingrese la ruta del archivo CSV: ").strip()
    
    # Verifica que el archivo exista en el sistema
    if not os.path.isfile(file_path):
        print(f"El archivo {file_path} no existe.")
        return  # Sale de la función si el archivo no existe
    
    # Intenta cargar el archivo CSV usando la función definida anteriormente
    df = load_csv_file(file_path)
    if df is None:
        return  # Sale de la función si hubo un error al cargar el archivo
    
    # Muestra información sobre el archivo cargado
    # df.shape[0] es el número de filas, df.shape[1] es el número de columnas
    print(f"Archivo cargado correctamente. Contiene {df.shape[0]} filas y {df.shape[1]} columnas.")
    
    # Intenta identificar la columna que contiene nombres de países
    country_column = find_country_column(df)
    if country_column is None:
        print("No se pudo identificar una columna de países en el archivo.")
        return  # Sale si no puede identificar la columna de países
    
    print(f"Columna de países identificada: {country_column}")
    
    # Busca columnas que representan años
    year_columns = find_year_columns(df)
    if not year_columns:
        print("No se encontraron columnas de años en el archivo.")
        return  # Sale si no encuentra columnas de años
    
    # Muestra las columnas de años identificadas
    # join concatena los elementos de la lista con comas
    print(f"Columnas de años identificadas: {', '.join(map(str, year_columns))}")
    
    # Obtiene la lista de países únicos del DataFrame y la ordena alfabéticamente
    # unique() devuelve los valores únicos de una columna
    countries = sorted(df[country_column].unique())
    
    # Muestra la lista numerada de países disponibles
    print("\nPaíses disponibles:")
    for i, country in enumerate(countries, 1):  # enumerate con start=1 para numerar desde 1
        print(f"{i}. {country}")
    
    # Bucle principal para que el usuario pueda seleccionar países
    while True:
        # Solicita al usuario que seleccione un país o presione 'q' para salir
        selection = input("\nIngrese el número o nombre del país (o 'q' para salir): ").strip()
        
        # Verifica si el usuario quiere salir
        if selection.lower() == 'q':
            break  # Sale del bucle si el usuario ingresa 'q'
        
        # Variable para almacenar el país seleccionado
        selected_country = None
        
        # Verifica si la selección es un número
        if selection.isdigit():
            # Convierte el número a índice (restando 1 porque la numeración empieza en 1)
            index = int(selection) - 1
            # Verifica que el índice sea válido
            if 0 <= index < len(countries):
                selected_country = countries[index]  # Asigna el país correspondiente
            else:
                # Mensaje de error si el número está fuera de rango
                print("Número inválido. Por favor, seleccione un número válido.")
                continue  # Vuelve al inicio del bucle
        else:
            # Si no es un número, busca países que contengan el texto ingresado
            # Crea una lista de países que coinciden parcialmente con la entrada
            matches = [country for country in countries if selection.lower() in country.lower()]
            
            # Verifica los resultados de la búsqueda
            if len(matches) == 1:
                # Si hay una única coincidencia, selecciona ese país
                selected_country = matches[0]
            elif len(matches) > 1:
                # Si hay múltiples coincidencias, muestra la lista y pide al usuario que elija
                print("Múltiples coincidencias encontradas:")
                for i, match in enumerate(matches, 1):
                    print(f"{i}. {match}")
                
                # Solicita al usuario que seleccione uno de los países coincidentes
                sub_selection = input("Seleccione el número del país: ").strip()
                
                # Verifica si la selección es un número
                if sub_selection.isdigit():
                    # Convierte a índice
                    sub_index = int(sub_selection) - 1
                    # Verifica que el índice sea válido
                    if 0 <= sub_index < len(matches):
                        selected_country = matches[sub_index]  # Asigna el país seleccionado
                    else:
                        print("Número inválido.")
                        continue  # Vuelve al inicio del bucle
                else:
                    print("Entrada inválida.")
                    continue  # Vuelve al inicio del bucle
            else:
                # Si no hay coincidencias, muestra un mensaje y vuelve al inicio
                print(f"No se encontró ningún país que coincida con '{selection}'.")
                continue  # Vuelve al inicio del bucle
        
        # Una vez que se ha seleccionado un país válido, genera el gráfico
        print(f"\nGenerando gráfico para {selected_country}...")
        
        # Llama a la función para generar el gráfico y almacena el resultado
        success = plot_country_population(df, country_column, year_columns, selected_country)
        
        # Verifica si el gráfico se generó correctamente
        if not success:
            print("No se pudo generar el gráfico.")


# Punto de entrada del programa
# Verifica si este archivo se está ejecutando directamente (no importado como módulo)
if __name__ == "__main__":
    main()  # Llama a la función principal