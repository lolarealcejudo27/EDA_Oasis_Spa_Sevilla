import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def run_analysis():
    print("🚀 Ejecutando análisis final...")
    if not os.path.exists('src/img'): os.makedirs('src/img')

    try:
        # Cargamos saltando la fila de título
        df = pd.read_csv('src/data/informe_ventas.csv', skiprows=1)
    except Exception as e:
        print(f"❌ No se encuentra el CSV: {e}")
        return

    # Limpiamos nombres de columnas a minúsculas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # BUSCADOR DINÁMICO: En lugar de usar nombres fijos, buscamos "algo que se parezca"
    def encontrar_columna(lista_palabras, df):
        for col in df.columns:
            if any(palabra in col for palabra in lista_palabras):
                return col
        return None

    col_fecha = encontrar_columna(['fecha', 'creado'], df)
    col_neto = encontrar_columna(['neto', 'total'], df)
    col_cp = encontrar_columna(['postal', 'codigo'], df)

    if not col_fecha or not col_neto:
        print(f"❌ Error: No encontré las columnas. Columnas actuales: {df.columns.tolist()}")
        return

    # Limpieza de datos
    df[col_neto] = pd.to_numeric(df[col_neto].astype(str).str.replace('€', '').str.replace('.', '').str.replace(',', '.').strip(), errors='coerce')
    df['fecha_dt'] = pd.to_datetime(df[col_fecha].astype(str).str.replace(' a las ', ' '), errors='coerce')

    # GRÁFICO DE ESTACIONALIDAD
    plt.figure(figsize=(10, 5))
    df_plot = df.dropna(subset=['fecha_dt', col_neto])
    df_plot.groupby(df_plot['fecha_dt'].dt.to_period('M'))[col_neto].sum().plot(kind='line', marker='o', color='teal')
    plt.title('Ventas Mensuales')
    plt.tight_layout()
    plt.savefig('src/img/01_limpieza_y_estacionalidad.png')
    plt.close()

    print(f"✅ ¡CONSEGUIDO! Imágenes guardadas en src/img/")
    print(f"Columnas usadas: {col_fecha} y {col_neto}")

if __name__ == "__main__":
    run_analysis()
    