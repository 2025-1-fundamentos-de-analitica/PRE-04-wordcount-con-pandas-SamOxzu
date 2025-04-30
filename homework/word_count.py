"""Taller evaluable"""

import glob
import os

import pandas as pd  # type: ignore


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    # Obtiene la lista de archivos en el directorio de entrada
    files = glob.glob(f"{input_directory}/*")
    # Comprenhension que recorre todos los archivos en la carpeta input
    dataframes = [
        # Lee cada archivo y lo almacena en un DataFrame de Pandas
        pd.read_csv(
            file,
            header=None,
            delimiter="\t",
            names=["line"],
            index_col=None,
        )
        for file in files
    ]

    # Concatena todos los DataFrames en uno solo
    dataframe = pd.concat(dataframes, ignore_index=True)

    return dataframe


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    # Crea una copia del DataFrame para evitar modificar el original
    dataframe = dataframe.copy()
    # Convierte la columna "line" a minúsculas
    dataframe["line"] = dataframe["line"].str.lower()
    # Elimina los signos de puntuación (coma y punto)
    dataframe["line"] = (
        dataframe["line"]
        .str.replace(",", "")
        .str.replace(".", "")
    )
    return dataframe


def count_words(dataframe):
    """Word count"""
    # Crea una copia del DataFrame para evitar modificar el original
    dataframe = dataframe.copy()
    # Divide cada columna "line" en una lista de palabras (separadas por espacios)
    dataframe["line"] = dataframe["line"].str.split()
    # Expande la lista de palabras de manera que cada palabra ocupe una fila, acompañada
    # por su número de registro (de la linea que salió).
    dataframe = dataframe.explode("line")
    # Agrupa por palabra (groupby) y cuenta el número de ocurrencias (size) de cada una
    # por último, resetea el índice y renombra la columna de conteo a "count" (reset_index).
    dataframe = dataframe.groupby("line").size().reset_index(name="count")
    return dataframe


def save_output(dataframe, output_directory):
    """Save output to a file."""

    # Si no existe el directorio de salida, lo crea.
    # Si existe, elimina todos los archivos y el directorio.
    # Luego lo vuelve a crear.
    if os.path.exists(output_directory):
        files = glob.glob(f"{output_directory}/*")
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)

    os.makedirs(output_directory)

    # Guarda el dataframe en un .csv
    dataframe.to_csv(
        f"{output_directory}/part-00000", # nombre del archivo de salida
        sep="\t", # separador de columnas (tabulador)
        index=False, # no guardar el índice
        header=False, # no guardar el encabezado
    )


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""

    # Crea un archivo vacío llamado _SUCCESS en el directorio de salida
    # para indicar que el trabajo se ha completado con éxito.
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_directory)
    create_marker(output_directory)


if __name__ == "__main__":

    run_job(
        "files/input",
        "files/output",
    )