# Importamos el módulo csv que proporciona funcionalidades para trabajar con archivos CSV
import csv
# Importamos matplotlib para crear gráficas
import matplotlib.pyplot as plt
# Importamos numpy para operaciones numéricas
import numpy as np

def leer_csv(nombre_archivo):
    """
    Función que lee un archivo CSV y muestra su contenido
    
    Args:
        nombre_archivo (str): Ruta al archivo CSV
        
    Returns:
        tuple: (encabezados, datos) donde encabezados es una lista con los nombres de columnas
               y datos es una lista de filas del archivo CSV
    """
    try:
        # Abrimos el archivo CSV en modo lectura ('r')
        # newline='' evita problemas con diferentes terminaciones de línea en distintos sistemas operativos
        # encoding='utf-8' asegura que se manejen correctamente caracteres especiales
        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
            
            # Creamos un objeto lector CSV que nos permitirá procesar el archivo línea por línea
            lector_csv = csv.reader(archivo_csv)
            
            # Leemos la primera línea que normalmente contiene los encabezados de las columnas
            # next() avanza el iterador y devuelve el siguiente valor (en este caso, la primera fila)
            encabezados = next(lector_csv)
            
            # Imprimimos los encabezados para mostrar la estructura del archivo
            print(f"Encabezados: {encabezados}")
            
            # Creamos una lista vacía para almacenar todas las filas de datos
            datos = []
            
            # Recorremos cada fila restante en el archivo CSV
            # El lector_csv es un iterador que va entregando cada línea como una lista
            for fila in lector_csv:
                # Añadimos cada fila a nuestra lista de datos
                datos.append(fila)
                
                # Imprimimos cada fila para visualizar los datos
                print(fila)
                
            # Una vez leídas todas las filas, mostramos el total para tener una idea del tamaño del archivo
            print(f"\nTotal de filas: {len(datos)}")
            
            # Devolvemos tanto los encabezados como los datos para poder usarlos en la visualización
            return encabezados, datos
    
    except FileNotFoundError:
        # Capturamos el error específico que ocurre cuando el archivo no existe
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        # Devolvemos listas vacías para mantener la consistencia del tipo de retorno
        return [], []
    
    except Exception as e:
        # Capturamos cualquier otro error que pueda ocurrir durante la lectura
        print(f"Error al leer el archivo: {e}")
        # Devolvemos listas vacías para mantener la consistencia del tipo de retorno
        return [], []

def crear_grafica_barras(encabezados, datos, columna_x=0, columna_y=1):
    """
    Crea una gráfica de barras con los datos del CSV
    
    Args:
        encabezados (list): Lista con los nombres de columnas
        datos (list): Lista de filas con los datos
        columna_x (int): Índice de la columna a usar en el eje X (por defecto 0)
        columna_y (int): Índice de la columna a usar en el eje Y (por defecto 1)
    """
    try:
        # Verificamos que tengamos suficientes columnas en los datos
        if len(encabezados) <= max(columna_x, columna_y):
            print(f"Error: No hay suficientes columnas. El archivo tiene {len(encabezados)} columnas.")
            return
        
        # Verificamos que tengamos datos
        if not datos:
            print("Error: No hay datos para graficar.")
            return
        
        # Extraemos los valores para los ejes X e Y
        # Para el eje X, usamos la columna especificada
        etiquetas_x = [fila[columna_x] for fila in datos if len(fila) > columna_x]
        
        # Para el eje Y, intentamos convertir los valores a números
        valores_y = []
        for fila in datos:
            if len(fila) > columna_y:
                try:
                    # Intentamos convertir el valor a número
                    valores_y.append(float(fila[columna_y]))
                except ValueError:
                    # Si no se puede convertir, usamos 0
                    print(f"Advertencia: No se pudo convertir '{fila[columna_y]}' a número. Se usará 0.")
                    valores_y.append(0)
        
        # Creamos la figura y el eje para la gráfica
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Generamos las posiciones para las barras
        x = np.arange(len(etiquetas_x))
        
        # Creamos la gráfica de barras
        barras = ax.bar(x, valores_y, width=0.6, color='skyblue', edgecolor='black')
        
        # Personalizamos la gráfica
        ax.set_xlabel(encabezados[columna_x])  # Etiqueta eje X
        ax.set_ylabel(encabezados[columna_y])  # Etiqueta eje Y
        ax.set_title(f'Gráfica de {encabezados[columna_y]} por {encabezados[columna_x]}')  # Título
        ax.set_xticks(x)  # Posiciones de las etiquetas
        
        # Si hay muchas etiquetas, las rotamos para mejor visualización
        if len(etiquetas_x) > 5:
            ax.set_xticklabels(etiquetas_x, rotation=45, ha='right')
        else:
            ax.set_xticklabels(etiquetas_x)
        
        # Añadimos una cuadrícula para facilitar la lectura
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Añadimos los valores encima de cada barra
        for i, v in enumerate(valores_y):
            ax.text(i, v + 0.1, str(round(v, 2)), ha='center')
        
        # Ajustamos el diseño para evitar recortes
        plt.tight_layout()
        
        # Mostramos la gráfica
        plt.show()
        
    except Exception as e:
        print(f"Error al crear la gráfica: {e}")

# Punto de entrada cuando el script se ejecuta directamente (no cuando se importa)
if __name__ == "__main__":
    # Definimos el nombre del archivo CSV que queremos leer
    # Este valor debe cambiarse para que coincida con el archivo que se desea procesar
    nombre_archivo = './app/data2.csv'
    
    # Llamamos a nuestra función para leer el archivo CSV
    encabezados, datos = leer_csv(nombre_archivo)
    
    # Si tenemos datos, creamos la gráfica de barras
    if encabezados and datos:
        print("\nCreando gráfica de barras...")
        # Por defecto usamos la primera columna para el eje X y la segunda para el eje Y
        # Estos valores pueden ajustarse según el contenido del CSV
        crear_grafica_barras(encabezados, datos, columna_x=0, columna_y=1)