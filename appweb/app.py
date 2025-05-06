# Importamos las bibliotecas necesarias
from flask import Flask, render_template, jsonify  # Flask para crear la aplicación web, render_template para renderizar HTML, jsonify para respuestas JSON
import random  # Módulo para generar números aleatorios
import time  # Módulo para trabajar con marcas de tiempo

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)  # '__name__' indica el nombre del módulo actual, usado por Flask para localizar recursos como plantillas y archivos estáticos

# Definimos la ruta principal de la aplicación
@app.route('/')  # Decorador que asocia esta función con la URL raíz ('/')
def index():
    # Renderiza y devuelve el archivo 'index.html' ubicado en la carpeta 'templates'
    return render_template('index.html')

# Definimos una ruta para obtener datos aleatorios
@app.route('/get_random_data')  # Decorador que asocia esta función con la URL '/get_random_data'
def get_random_data():
    # Genera un número aleatorio de tipo float entre 0 y 100, redondeado a 2 decimales
    random_value = round(random.uniform(0, 100), 2)
    # Devuelve una respuesta JSON con el número aleatorio ('value') y la marca de tiempo actual ('timestamp')
    return jsonify({'value': random_value, 'timestamp': time.time()})

# Punto de entrada principal de la aplicación
if __name__ == '__main__':  # Verifica si el archivo se está ejecutando directamente (no importado como módulo)
    # Inicia el servidor Flask en modo de depuración
    # El modo de depuración permite reiniciar automáticamente el servidor al realizar cambios en el código
    # También muestra mensajes de error detallados en el navegador
    app.run(debug=True)