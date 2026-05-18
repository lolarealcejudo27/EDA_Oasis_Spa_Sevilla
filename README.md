# EDA Oasis Spa Sevilla

Análisis Exploratorio de Datos (EDA) sobre los registros de **ventas y reservas** del Oasis Spa de Sevilla, con el objetivo de **caracterizar el perfil de consumo de su clientela** y aportar evidencia que ayude a optimizar la estrategia comercial: dónde están los clientes más frecuentes, cuándo compran más, qué producto lidera cada mes y si la base instalada repite o explora servicios nuevos.

Proyecto del bootcamp **Data Science Online — The Bridge** (Project Break I).

---

## Hipótesis planteadas

El análisis se estructura en torno a cuatro hipótesis verificables, dos sobre el bloque de **ventas** y dos sobre el bloque de **productos**:

| # | Bloque | Hipótesis |
|---|--------|-----------|
| **H1** | Ventas | Existe una concentración geográfica clara: una minoría de zonas (códigos postales / países) explica la mayoría de las reservas recurrentes. |
| **H2** | Ventas | El volumen de ventas presenta una estacionalidad positiva marcada en determinados meses del año. |
| **H3** | Productos | Existe un producto líder mensual ("top-of-mind") que captura la mayor parte de las reservas en cada mes. |
| **H4** | Productos | La base de clientes recurrentes se inclina más hacia la **repetición del mismo servicio** que hacia el **cross-selling** (probar productos nuevos). |

Cada hipótesis se contrasta en su notebook correspondiente dentro de `src/notebooks/` y se consolida en `main.ipynb`.

---

## Tecnologías utilizadas

- **Python 3.11+**
- **pandas** — manipulación y limpieza de datos
- **matplotlib** y **seaborn** — visualización
- **Jupyter Notebook** — análisis interactivo
- **Git / GitHub** — control de versiones y trabajo colaborativo (Gitflow con ramas `explorador_*`)

---

## Estructura del repositorio

```
EDA_Oasis_Spa_Sevilla/
├── README.md                  ← este archivo
├── main.ipynb                 ← versión final consolidada del EDA  [pendiente]
├── Memoria.pdf                ← memoria técnica (10–15 pp.)         [pendiente]
├── Presentacion.pdf           ← presentación ejecutiva              [pendiente]
├── .gitignore
└── src/
    ├── data/                  ← datos brutos
    │   ├── informe_reservas.csv
    │   └── informe_ventas.csv
    ├── img/                   ← gráficos generados
    │   ├── 01_limpieza_y_estacionalidad.png
    │   ├── 02_geografia_top20.png
    │   ├── 03_producto_estrella_ingresos.png
    │   ├── 03_producto_volumen.png
    │   └── 04_analisis_retencion.png
    ├── notebooks/             ← notebooks de exploración por hipótesis
    │   ├── 01_limpieza_y_estacionalidad.ipynb
    │   ├── 02_geografia.ipynb
    │   ├── 03_producto_estrella.ipynb
    │   └── 04_retencion_y_cross_selling.ipynb
    └── utils/
        └── funciones.py       ← funciones auxiliares reutilizables
```

---

## Instrucciones de reproducción

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/<usuario>/EDA_Oasis_Spa_Sevilla.git
   cd EDA_Oasis_Spa_Sevilla
   ```

2. **Crea un entorno virtual** e instala las dependencias

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate

   pip install pandas matplotlib seaborn jupyter
   ```

3. **Abre el notebook consolidado**

   ```bash
   jupyter notebook main.ipynb
   ```

   Para revisar el análisis por hipótesis individualmente, los notebooks de desarrollo están en `src/notebooks/`.

> **Nota sobre los datos:** los CSV de `src/data/` contienen información personal (emails y códigos postales reales). Antes de hacer el repositorio público se aplicará un proceso de **anonimización** (hash de emails y agregación de códigos postales a nivel de provincia). El análisis se realiza sobre los campos agregados, sin trazabilidad individual.

---

## Principales conclusiones

> *Sección pendiente de redacción definitiva — se completará al cerrar el análisis.*

- **H1 — Geografía:** `[TODO: confirmada / refutada · evidencia principal]`
- **H2 — Estacionalidad:** `[TODO: confirmada / refutada · meses pico identificados]`
- **H3 — Producto estrella:** `[TODO: confirmada / refutada · producto(s) líder por mes]`
- **H4 — Retención vs. cross-selling:** `[TODO: confirmada / refutada · ratio observado]`

**Recomendaciones de negocio:** `[TODO]`

---

## Autores

| | Nombre | GitHub | LinkedIn |
|---|---|---|---|
| | Miguel Coxon | [@MCCFern](https://github.com/MCCFern) | [TODO] |
| | Lola Real Cejudo | [@lolarealcejudo27](https://github.com/lolarealcejudo27) | [TODO] |

---

*Proyecto desarrollado en el marco del bootcamp Data Science Online de [The Bridge](https://www.thebridge.tech/).*
