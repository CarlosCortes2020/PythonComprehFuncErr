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
                
            # Una vez leídas todas las filas, mostramos el total para tener una idea del tamaño del archivo
            print(f"\nTotal de filas: {len(datos)}")
            
            # Mostramos las primeras 5 filas (o menos si hay menos datos) para visualizar el contenido
            print("\nVista previa de los datos:")
            for i, fila in enumerate(datos[:5]):
                print(f"Fila {i+1}: {fila}")
            
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

def seleccionar_columnas(encabezados):
    """
    Permite al usuario seleccionar qué columnas quiere usar para la gráfica
    
    Args:
        encabezados (list): Lista con los nombres de columnas
        
    Returns:
        tuple: (columna_x, columna_y) índices de las columnas seleccionadas
    """
    # Mostramos las columnas disponibles
    print("\nColumnas disponibles:")
    for i, columna in enumerate(encabezados):
        print(f"{i}: {columna}")
    
    try:
        # Solicitamos al usuario la columna para el eje X (etiquetas)
        while True:
            columna_x = int(input("\nSeleccione el número de la columna para el eje X (etiquetas): "))
            if 0 <= columna_x < len(encabezados):
                break
            else:
                print(f"Valor inválido. Debe ser un número entre 0 y {len(encabezados)-1}")
        
        # Solicitamos al usuario la columna para el eje Y (valores)
        while True:
            columna_y = int(input("Seleccione el número de la columna para el eje Y (valores numéricos): "))
            if 0 <= columna_y < len(encabezados):
                break
            else:
                print(f"Valor inválido. Debe ser un número entre 0 y {len(encabezados)-1}")
        
        return columna_x, columna_y
    
    except ValueError:
        print("Error: Debe ingresar números enteros.")
        # Si hay un error, devolvemos valores por defecto
        return 0, 1

def crear_grafica_barras(encabezados, datos, columna_x, columna_y, titulo=None):
    """
    Crea una gráfica de barras con los datos del CSV
    
    Args:
        encabezados (list): Lista con los nombres de columnas
        datos (list): Lista de filas con los datos
        columna_x (int): Índice de la columna a usar en el eje X
        columna_y (int): Índice de la columna a usar en el eje Y
        titulo (str, optional): Título personalizado para la gráfica
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
        errores = 0
        for fila in datos:
            if len(fila) > columna_y:
                try:
                    # Intentamos convertir el valor a número
                    valores_y.append(float(fila[columna_y]))
                except ValueError:
                    # Si no se puede convertir, usamos 0
                    errores += 1
                    valores_y.append(0)
        
        if errores > 0:
            print(f"Advertencia: {errores} valores no pudieron convertirse a números y se establecieron como 0.")
        
        # Creamos la figura y el eje para la gráfica
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Generamos las posiciones para las barras
        x = np.arange(len(etiquetas_x))
        
        # Creamos la gráfica de barras
        barras = ax.bar(x, valores_y, width=0.6, color='skyblue', edgecolor='black')
        
        # Personalizamos la gráfica
        ax.set_xlabel(encabezados[columna_x])  # Etiqueta eje X
        ax.set_ylabel(encabezados[columna_y])  # Etiqueta eje Y
        
        # Establecemos el título, ya sea el personalizado o uno automático
        if titulo:
            ax.set_title(titulo)
        else:
            ax.set_title(f'Gráfica de {encabezados[columna_y]} por {encabezados[columna_x]}')
        
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
            ax.text(i, v + max(valores_y)*0.01, str(round(v, 2)), ha='center')
        
        # Ajustamos el diseño para evitar recortes
        plt.tight_layout()
        
        # Mostramos la gráfica
        plt.show()
        
    except Exception as e:
        print(f"Error al crear la gráfica: {e}")

def menu_principal():
    """
    Función principal que muestra un menú interactivo para trabajar con archivos CSV
    """
    while True:
        print("\n==== MENÚ PRINCIPAL ====")
        print("1. Cargar archivo CSV")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            # Solicitamos el nombre del archivo
            nombre_archivo = input("\nIntroduzca el nombre del archivo CSV: ")
            
            # Leemos el archivo
            encabezados, datos = leer_csv(nombre_archivo)
            
            # Si tenemos datos, mostramos el menú de gráficas
            if encabezados and datos:
                menu_graficas(encabezados, datos)
                
        elif opcion == "2":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción no válida. Inténtelo de nuevo.")

def menu_graficas(encabezados, datos):
    """
    Muestra un menú para trabajar con gráficas
    
    Args:
        encabezados (list): Lista con los nombres de columnas
        datos (list): Lista de filas con los datos
    """
    while True:
        print("\n==== MENÚ DE GRÁFICAS ====")
        print("1. Crear gráfica de barras")
        print("2. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            # Permitimos al usuario seleccionar las columnas
            columna_x, columna_y = seleccionar_columnas(encabezados)
            
            # Preguntamos si desea un título personalizado
            usar_titulo_personalizado = input("\n¿Desea especificar un título personalizado? (s/n): ").lower() == 's'
            titulo = None
            if usar_titulo_personalizado:
                titulo = input("Introduzca el título de la gráfica: ")
            
            # Creamos la gráfica con los parámetros seleccionados
            print("\nCreando gráfica de barras...")
            crear_grafica_barras(encabezados, datos, columna_x, columna_y, titulo)
            
        elif opcion == "2":
            return
        else:
            print("\nOpción no válida. Inténtelo de nuevo.")

# Punto de entrada cuando el script se ejecuta directamente (no cuando se importa)
if __name__ == "__main__":
    # Iniciamos el programa con el menú principal
    menu_principal()