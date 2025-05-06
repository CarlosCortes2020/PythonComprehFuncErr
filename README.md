# PythonComprehFuncErr

Este repositorio contiene un conjunto de programas y ejemplos prácticos desarrollados en Python. Los ejercicios están enfocados en el uso de **comprehensions**, **funciones** y el **manejo de errores**, conceptos fundamentales para el desarrollo de software en Python. Este proyecto forma parte del curso [Python: Comprehensions, Funciones y Manejo de Errores](https://platzi.com/cursos/python-funciones/) ofrecido por Platzi.

## Contenido del Repositorio

### 1. **Aplicación Web con Flask**
- **Descripción**: Una aplicación web interactiva que utiliza Flask para mostrar datos aleatorios en tiempo real mediante un gráfico dinámico.
- **Archivos principales**:
  - `appweb/app.py`: Código principal de la aplicación Flask.
  - `appweb/templates/index.html`: Plantilla HTML que incluye un gráfico dinámico creado con Chart.js.
- **Características**:
  - Generación de datos aleatorios en el servidor.
  - Visualización en tiempo real de los datos mediante un gráfico de líneas.
  - Interacción con botones para iniciar y detener la actualización de datos.

### 2. **Procesamiento de Datos con Pandas**
- **Descripción**: Scripts que demuestran cómo trabajar con archivos CSV utilizando la biblioteca Pandas.
- **Archivos principales**:
  - `testes.py`: Contiene funciones para:
    - Cargar y procesar datos desde archivos CSV.
    - Identificar columnas específicas, como nombres de países y años.
    - Generar gráficos basados en los datos procesados.
- **Características**:
  - Uso de expresiones regulares para identificar patrones en los encabezados de columnas.
  - Manejo de errores al cargar y procesar datos.

### 3. **Ejercicios de Python**
- **Descripción**: Ejercicios prácticos que exploran el uso de comprehensions, funciones y manejo de errores.
- **Características**:
  - Uso de **list comprehensions**, **set comprehensions** y **dictionary comprehensions**.
  - Implementación de funciones reutilizables y manejo de excepciones para garantizar la robustez del código.

## Requisitos Previos
Para ejecutar los scripts y la aplicación web, asegúrate de tener instalados los siguientes componentes:
- **Python 3.8 o superior**
- Bibliotecas requeridas:
  - `Flask`
  - `pandas`
  - `matplotlib`
  - `Chart.js` (incluido en la plantilla HTML)

Puedes instalar las dependencias necesarias ejecutando:
```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```
