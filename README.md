# EDA Oasis Spa Sevilla

Análisis Exploratorio de Datos (EDA) sobre 24 meses de **ventas y reservas** del Oasis Spa de Sevilla (mayo de 2024 – abril de 2026: **8.186 operaciones · 5.746 clientes únicos · 23 productos**), con el objetivo de **caracterizar el perfil de consumo de su clientela** y aportar evidencia para optimizar la estrategia comercial: dónde están los clientes más frecuentes, cuándo compran más, qué producto lidera cada mes y si la base instalada repite o explora servicios nuevos.

Proyecto del bootcamp **Data Science Online — The Bridge** (Project Break I).

---

## Hipótesis planteadas

El análisis se estructura en torno a cuatro hipótesis verificables:

| # | Bloque | Hipótesis | Notebook |
|---|--------|-----------|----------|
| **H1** | Ventas | Existe una concentración geográfica clara: una minoría de zonas explica la mayoría de las reservas recurrentes. | `01_geografia.ipynb` |
| **H2** | Ventas | El volumen de ventas presenta una estacionalidad positiva marcada en determinados meses del año. | `02_estacionalidad.ipynb` |
| **H3** | Productos | Existe un producto líder mensual ("top-of-mind") que captura la mayor parte de las reservas en cada mes. | `03_producto_estrella.ipynb` |
| **H4** | Productos | La base de clientes recurrentes se inclina más hacia la **repetición del mismo servicio** que hacia el **cross-selling**. | `04_retencion_y_cross_selling.ipynb` |

Cada hipótesis se contrasta en su notebook correspondiente y se consolida en `main.ipynb`.

---

## Principales conclusiones

| H | Veredicto | Cifras clave |
|---|---|---|
| **H1 — Geografía** | ✅ **CONFIRMADA** (con limitación) | Sevilla concentra el **67,6 %** de las operaciones recurrentes con CP español válido; Andalucía completa el **84,8 %**. Un **12,4 %** de las operaciones globales son internacionales (FR, GB, US, IT al frente). *Limitación: solo el 3,4 % de las operaciones recurrentes tiene CP válido en el dato.* |
| **H2 — Estacionalidad** | ✅ **CONFIRMADA** | Pico en **enero** (índice 167 sobre media 100), valle en **mayo** (64). *Spread pico/valle = **2,6×***. Q4 + enero-febrero son los meses fuertes; mayo-agosto el valle estructural. |
| **H3 — Producto estrella** | 🟡 **MATIZADA** | **5 productos** distintos lideran a lo largo de 24 meses (no hay top-of-mind único): *¡Tarjeta de regalo!* (8 meses), *Ritual Oasis Silver* (7), *Bronze* (4), *Experiencia Termal* (4), *Gold* (1). La cuota media del líder mensual es **~24 %**; solo en diciembre se acerca al 50 %. |
| **H4 — Retención vs. cross-selling** | ❌ **REFUTADA** | Entre recurrentes, **cross-selling 51,9 % vs. leal 48,1 %** — la inclinación es a explorar, no a repetir. El hallazgo dominante: **78,5 % de la base son clientes ocasionales** (4.508 de 5.746). |

### Recomendaciones de negocio (resumen)

1. **Conversión "primera visita → segunda visita"** es la mayor palanca de crecimiento (78,5 % de ocasionales sin retorno en 24 meses).
2. **Activar el valle estival** (mayo-agosto) con propuestas dirigidas al residente sevillano: tratamientos frescos, packs *tarde-noche*, descuentos mid-week.
3. **Planificación operativa del pico nov-feb** (capacidad, stock de tarjetas regalo, inversión publicitaria concentrada).
4. **Estrategia hiperlocal en CP 41xxx** y comunicación bilingüe (EN/FR) para el segmento turístico internacional.
5. **Calendario de producto rotatorio** en lugar de un único *hero product*.

Las recomendaciones priorizadas y desarrolladas están en `Memoria.pdf` (sección 8).

---

## Tecnologías utilizadas

- **Python 3.11+**
- **pandas** — manipulación y limpieza de datos
- **matplotlib** y **seaborn** — visualización
- **Jupyter Notebook** — análisis interactivo
- **Git / GitHub** — control de versiones colaborativo (ramas `explorador_*`)

---

## Estructura del repositorio

```
EDA_Oasis_Spa_Sevilla/
├── README.md                                  ← este archivo
├── main.ipynb                                 ← EDA consolidado (versión final)
├── Memoria.pdf                                ← memoria técnica (10-15 pp.)
├── Presentación.pdf                           ← presentación ejecutiva
├── Memoria tecnica.docx                       ← fuente editable de la memoria (ignorada por git)
├── .gitignore
├── .vscode/
└── src/
    ├── data/                                  ← datos brutos (NO versionados — ver privacidad)
    ├── img/                                   ← gráficos generados por los notebooks
    │   ├── 01_geografia_top_areas.png
    │   ├── 01_geografia_sevilla.png
    │   ├── 01_geografia_internacional.png
    │   ├── 02_estacionalidad.png
    │   ├── 02_indice_estacionalidad.png
    │   ├── 03_producto_estrella_ingresos.png
    │   ├── 03_producto_volumen.png
    │   ├── 03_producto_heatmap_mensual.png
    │   ├── 03_producto_meses_como_lider.png
    │   ├── 04_analisis_retencion.png
    │   └── 04_reparto_clientes.png
    ├── notebooks/                             ← notebooks de exploración (uno por hipótesis)
    │   ├── 01_geografia.ipynb
    │   ├── 02_estacionalidad.ipynb
    │   ├── 03_producto_estrella.ipynb
    │   └── 04_retencion_y_cross_selling.ipynb
    └── utils/
        ├── funciones.py                       ← utilidades reutilizables (anonimización, limpieza)
        ├── _build_memoria.py                  ← generador one-shot del .docx de la memoria
        ├── borrador.txt                       ← preguntas originales del cliente (artefacto histórico)
        └── main.py                            ← script de prototipado (no usado en el flujo final)
```

---

## Privacidad y reproducibilidad

Los CSV originales (`informe_ventas.csv` e `informe_reservas.csv`) contienen información personal identificable (emails y códigos postales reales) y **no se versionan en el repositorio** (ver `.gitignore`).

La anonimización se aplica **in-memory al inicio de cada notebook** mediante `src/utils/funciones.py::anonimizar()`:

- `email` → `cliente_id` (entero secuencial). El mapping es global a todas las DataFrames, por lo que un mismo cliente recibe siempre el mismo identificador en ventas y en reservas. Esto permite seguir analizando retención y cross-selling sobre datos anonimizados.
- `codigo_postal_de_tarjeta_de_credito` → `cp_area` (3 primeros dígitos, equivalente a provincia + zona). Los CP no españoles se descartan.

**Para reproducir el análisis** se necesitan los dos CSV originales. Quienes deseen replicar el estudio deben contactar con los autores para obtener los datos (sujeto a las condiciones que acuerde el cliente). Sin los CSV, los notebooks fallarán al cargar.

---

## Instrucciones de reproducción

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/lolarealcejudo27/EDA_Oasis_Spa_Sevilla.git
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

3. **Coloca los CSV originales** en `src/data/` con los nombres:
   - `src/data/informe_ventas.csv`
   - `src/data/informe_reservas.csv`

4. **Ejecuta el notebook consolidado**

   ```bash
   jupyter notebook main.ipynb
   ```

   Para revisar el análisis hipótesis por hipótesis, los notebooks de desarrollo están en `src/notebooks/`. Todos comparten utilidades desde `src/utils/funciones.py`.

---

## Autores

| Nombre | GitHub |
|---|---|---|
| Miguel Coxon Fernández | [@MCCFern](https://github.com/MCCFern)|
| Lola Real Cejudo | [@lolarealcejudo27](https://github.com/lolarealcejudo27)|

---

*Proyecto desarrollado en el marco del bootcamp Data Science Online de [The Bridge](https://www.thebridge.tech/) — Project Break I (EDA). Mayo de 2026.*
