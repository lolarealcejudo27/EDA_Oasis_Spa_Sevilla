"""Funciones auxiliares para el EDA del Oasis Spa Sevilla."""

import pandas as pd

# Códigos de provincia españoles válidos (01 Álava … 52 Melilla)
_PROVINCIAS_ES = {str(i).zfill(2) for i in range(1, 53)}


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
