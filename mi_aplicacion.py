import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, filedialog, simpledialog
from datetime import datetime, timedelta
import tkinter as tk

def seleccionar_archivo():
    root = Tk()
    root.withdraw()
    archivo_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("CSV files", "*.csv")])
    root.destroy()
    return archivo_path

def leer_csv(archivo_path):
    return pd.read_csv(archivo_path)

def graficar_datos(df, intervalo, tolerancia):
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df.set_index('Fecha', inplace=True)

    patrones = {
        "A": [1, -1, 1, -1, 1],
        "B": [-1, 1, -1, 1, -1],
    }

    def calcular_similitud(serie, patron):
        n = len(patron)
        serie_normalizada = (serie - serie.mean()) / serie.std()
        patron_normalizado = (patron - np.mean(patron)) / np.std(patron)
        correlacion = np.correlate(serie_normalizada, patron_normalizado, mode='valid')
        return correlacion[0]

    resultados = []
    for patron_nombre, patron in patrones.items():
        similitud = calcular_similitud(df['Valor'].values[:len(patron)], patron)
        resultados.append((patron_nombre, similitud))

    patron_mas_similar = max(resultados, key=lambda x: x[1])

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Valor'], label='Datos')

    plt.scatter(df.index[0], df['Valor'].iloc[0], color='yellow', zorder=5)
    plt.scatter(df.index[-1], df['Valor'].iloc[-1], color='green', zorder=5)

    plt.title(f'Patrón más similar: {patron_mas_similar[0]} con similitud de {patron_mas_similar[1]:.2f}')
    plt.xlabel('Fecha')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    archivo_path = seleccionar_archivo()
    if not archivo_path:
        return
    
    df = leer_csv(archivo_path)

    root = Tk()
    root.withdraw()
    
    intervalo = simpledialog.askinteger("Intervalo de datos", "Seleccionar intervalo de datos (minutos):", minvalue=5, maxvalue=30)
    tolerancia = simpledialog.askfloat("Tolerancia", "Proporcionar margen de tolerancia (%):", minvalue=0, maxvalue=100)
    
    root.destroy()
    
    if intervalo and tolerancia is not None:
        graficar_datos(df, intervalo, tolerancia)

if __name__ == "__main__":
    main()
