"""Funciones auxiliares para el EDA del Oasis Spa Sevilla.

Este módulo centraliza la lógica reutilizable entre notebooks:

- :func:`limpiar_nombres_columnas` — normaliza nombres de columnas
- :func:`limpiar_moneda` — convierte strings con formato europeo ("1.200,50 €") a float
- :func:`parsear_mes_es` — parsea "January 2026" → datetime
- :func:`anonimizar` — sustituye email → cliente_id y CP → cp_area
"""

import pandas as pd

# Códigos de provincia españoles válidos (01 Álava … 52 Melilla)
_PROVINCIAS_ES = {str(i).zfill(2) for i in range(1, 53)}

# Mapeo Sí/No → 1/0 utilizado en columnas booleanas exportadas como texto
_MAPEO_BOOL = {"Sí": 1, "Si": 1, "S": 1, "Yes": 1,
               "No": 0, "N": 0}


def limpiar_nombres_columnas(df):
    """Normaliza los nombres de columnas: minúsculas, sin tildes ni signos.

    Convierte ``"¿Reprogramado?"`` en ``"reprogramado"``, etc. Útil para
    poder referenciar columnas de forma consistente y predecible.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame cuyos nombres de columna se quieren normalizar (se modifica
        in-place y se devuelve para encadenar).

    Returns
    -------
    pandas.DataFrame
        El mismo DataFrame con columnas normalizadas.
    """
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("¿", "", regex=False)
                  .str.replace("?", "", regex=False)
                  .str.replace(".", "", regex=False)
                  .str.replace("á", "a")
                  .str.replace("é", "e")
                  .str.replace("í", "i")
                  .str.replace("ó", "o")
                  .str.replace("ú", "u"))
    return df


def limpiar_moneda(valor):
    """Convierte una cadena monetaria europea a float.

    Acepta formatos como ``"1.200,50 €"``, ``"45,00"`` o ``"€ 12,30"`` y
    devuelve un float. Si el valor ya es numérico se devuelve tal cual.
    Valores no parseables devuelven ``NaN``.

    Parameters
    ----------
    valor : str | int | float
        Importe a limpiar.

    Returns
    -------
    float
        Valor numérico (``NaN`` si no es parseable).
    """
    if isinstance(valor, str):
        valor = (valor.replace("€", "")
                       .replace(".", "")
                       .replace(",", ".")
                       .strip())
    return pd.to_numeric(valor, errors="coerce")


def parsear_mes_es(serie):
    """Parsea una serie con formato ``"January 2026"`` a datetime.

    El backend del Oasis Spa exporta el mes en inglés. Esta función
    centraliza el parseo para evitar repetir ``format='%B %Y'`` en cada
    notebook. Las filas no parseables (p. ej. ``"24 meses"``) devuelven
    ``NaT``.

    Parameters
    ----------
    serie : pandas.Series
        Serie de strings con formato ``"Month YYYY"`` en inglés.

    Returns
    -------
    pandas.Series
        Serie de tipo ``datetime64[ns]``.
    """
    return pd.to_datetime(serie, format="%B %Y", errors="coerce")


def mapear_si_no(serie):
    """Convierte una serie con valores 'Sí'/'No' (y variantes) a 0/1.

    Acepta ``'Sí'``, ``'Si'``, ``'S'``, ``'Yes'`` como 1 y ``'No'``, ``'N'``
    como 0. Valores fuera del mapeo se devuelven como NaN (luego el notebook
    decide cómo imputarlos).

    Parameters
    ----------
    serie : pandas.Series
        Serie de strings.

    Returns
    -------
    pandas.Series
        Serie numérica con 0/1 y NaN en valores no reconocidos.
    """
    return serie.map(_MAPEO_BOOL)


def anonimizar(*dfs,
               email_cols=("email",),
               cp_cols=("codigo_postal_de_tarjeta_de_credito", "codigo_postal")):
    """Anonimiza una o varias DataFrames en bloque.

    - Sustituye los emails por ``cliente_id`` (entero secuencial). El mapping
      es global a todas las DataFrames pasadas, así un mismo cliente recibe
      siempre el mismo id sin importar en qué tabla aparezca → permite seguir
      analizando retención y cross-selling tras la anonimización.
    - Trunca los códigos postales a área (``cp_area``, 3 primeros dígitos)
      descartando CPs no españoles → conserva granularidad de área dentro de
      la provincia sin exponer la dirección exacta.

    Las columnas originales se eliminan tras la transformación.

    Parameters
    ----------
    *dfs : pandas.DataFrame
        Una o varias DataFrames a anonimizar.
    email_cols : tuple of str
        Nombres de columnas con emails a sustituir.
    cp_cols : tuple of str
        Nombres de columnas con CP a truncar.

    Returns
    -------
    pandas.DataFrame o tuple de pandas.DataFrame
        Una sola DataFrame si solo se pasó una, o una tupla en el mismo
        orden que la entrada.

    Examples
    --------
    >>> df_ventas, df_reservas = anonimizar(df_ventas, df_reservas)
    """
    # Mapping email -> cliente_id, global a todas las DFs
    emails = []
    for df in dfs:
        for col in email_cols:
            if col in df.columns:
                emails.append(df[col].dropna().astype(str))
    mapping = {}
    if emails:
        unicos = pd.concat(emails).drop_duplicates().reset_index(drop=True)
        mapping = {email: idx for idx, email in enumerate(unicos)}

    out = []
    for df in dfs:
        df = df.copy()
        for col in email_cols:
            if col in df.columns:
                df["cliente_id"] = df[col].astype(str).map(mapping).astype("Int64")
                df = df.drop(columns=[col])
        for col in cp_cols:
            if col in df.columns:
                s = df[col].astype("string").str.strip()
                area = s.where(s.str.len() > 0).str.zfill(5).str[:3]
                # Descarta CPs no españoles: los 2 primeros dígitos deben ser provincia válida
                df["cp_area"] = area.where(area.str[:2].isin(_PROVINCIAS_ES))
                df = df.drop(columns=[col])
        out.append(df)

    return tuple(out) if len(out) > 1 else out[0]
