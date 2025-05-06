# Paso 1: Importamos el módulo csv que proporciona funcionalidades para trabajar con archivos CSV
import csv

# Paso 2: Definimos una función para leer archivos CSV
def leer_csv(nombre_archivo):
    """
    Esta función abre y lee un archivo CSV, mostrando su contenido
    
    Args:
        nombre_archivo (str): El nombre o ruta del archivo CSV que queremos leer
    """
    try:
        # Paso 3: Abrimos el archivo CSV
        # El primer parámetro es el nombre del archivo
        # 'r' indica que lo abrimos en modo lectura
        # encoding='utf-8' ayuda a manejar caracteres especiales
        archivo = open(nombre_archivo, 'r', encoding='utf-8')
        
        # Paso 4: Creamos un objeto lector de CSV
        # Este objeto nos permite leer el archivo línea por línea
        lector_csv = csv.reader(archivo)
        
        # Paso 5: Leemos la primera línea que normalmente contiene los encabezados
        encabezados = next(lector_csv)
        print("Encabezados del archivo:")
        print(encabezados)
        
        # Paso 6: Leemos y mostramos el resto de líneas (los datos)
        print("\nDatos del archivo:")
        contador = 0
        for fila in lector_csv:
            print(fila)
            contador += 1
        
        # Paso 7: Mostramos cuántas filas de datos leímos
        print(f"\nTotal de filas de datos: {contador}")
        
        # Paso 8: Cerramos el archivo cuando terminamos de usarlo
        archivo.close()
        
    except FileNotFoundError:
        # Si el archivo no existe, mostramos un mensaje de error
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
    
    except Exception as e:
        # Si ocurre cualquier otro error, lo mostramos
        print(f"Error al leer el archivo: {e}")


# Paso 9: Código principal que ejecuta nuestra función
if __name__ == "__main__":
    # Nombre del archivo CSV que queremos leer
    archivo_csv = "./app/data.csv"
    
    # Llamamos a nuestra función
    leer_csv(archivo_csv)