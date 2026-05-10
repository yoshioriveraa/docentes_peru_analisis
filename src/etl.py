"""
etl.py
------
Pipeline ETL para el dataset de Docentes de IE Públicas del Perú.
Responsabilidades:
  - EXTRACT : carga el CSV crudo
  - TRANSFORM: limpieza, normalización y feature engineering
  - LOAD     : exporta el dataset limpio a SQLite y CSV procesado
"""

import sqlite3
import pandas as pd
import numpy as np


# ── Rutas ────────────────────────────────────────────────
RAW_PATH       = "data/raw/docentes_raw.csv"
PROCESSED_CSV  = "data/processed/docentes_clean.csv"
DB_PATH        = "data/processed/docentes.db"
TABLE_NAME     = "docentes"

# ── Columnas de grupos etarios ────────────────────────────
EDAD_COLS   = [
    "Docentes_25_menos_años",
    "Docentes_2635_años",
    "Docentes_3645_años",
    "Docentes_4655_años",
    "Docentes_5665_años",
    "Docentes_66_a_mas_años",
]
EDAD_LABELS = ["<=25", "26-35", "36-45", "46-55", "56-65", ">=66"]

# Columnas internas que no aportan al análisis
COLS_DROP = ["codlocal", "codgeo", "codooii", "area_censo",
             "region", "cod_mod", "anexo", "cen_edu"]


# ══════════════════════════════════════════════════════════
# 1. EXTRACT
# ══════════════════════════════════════════════════════════
def extract(path: str = RAW_PATH) -> pd.DataFrame:
    """Carga el CSV crudo y valida integridad básica."""
    df = pd.read_csv(path)
    print(f"[EXTRACT] {len(df):,} filas × {df.shape[1]} columnas cargadas")
    print(f"[EXTRACT] Valores nulos totales: {df.isnull().sum().sum()}")
    return df


# ══════════════════════════════════════════════════════════
# 2. TRANSFORM
# ══════════════════════════════════════════════════════════
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza, normalización y feature engineering."""
    df = df.copy()

    # 2.1 Limpiar strings
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # 2.2 Normalizar categorías (quitar prefijo numérico tipo "2.Primaria")
    for col in ["nivel", "nivel2", "nivel3", "area", "niv_mod"]:
        if col in df.columns:
            df[col + "_clean"] = df[col].str.replace(r"^\d+\.", "", regex=True).str.strip()

    # 2.3 Feature engineering
    total = df["Docentes_total"].replace(0, np.nan)

    df["pct_mujeres"]    = (df["Docentes_mujeres"]    / total * 100).round(2)
    df["pct_nombrados"]  = (df["Docentes_nombrados"]  / total * 100).round(2)
    df["pct_con_titulo"] = (df["Docentes_con_titulo"] / total * 100).round(2)
    df["pct_sin_titulo"] = (df["Docentes_sin_titulo"] / total * 100).round(2)

    df["ratio_nombrado_contratado"] = np.where(
        df["Docentes_contratados"] > 0,
        (df["Docentes_nombrados"] / df["Docentes_contratados"]).round(2),
        np.nan,
    )

    # Grupo etario predominante por IE
    df["grupo_edad_mayor"] = (
        df[EDAD_COLS]
        .idxmax(axis=1)
        .map(dict(zip(EDAD_COLS, EDAD_LABELS)))
    )

    # 2.4 Eliminar columnas redundantes
    df.drop(columns=[c for c in COLS_DROP if c in df.columns], inplace=True)

    print(f"[TRANSFORM] Shape final: {df.shape}")
    print(f"[TRANSFORM] Nuevas columnas: pct_mujeres, pct_nombrados, pct_con_titulo, "
          f"pct_sin_titulo, ratio_nombrado_contratado, grupo_edad_mayor")
    return df


# ══════════════════════════════════════════════════════════
# 3. LOAD
# ══════════════════════════════════════════════════════════
def load(df: pd.DataFrame,
         csv_path: str = PROCESSED_CSV,
         db_path: str = DB_PATH) -> sqlite3.Connection:
    """Guarda el dataset limpio en CSV y SQLite."""
    # CSV procesado
    df.to_csv(csv_path, index=False)
    print(f"[LOAD] CSV limpio guardado en: {csv_path}")

    # SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    print(f"[LOAD] Base de datos SQLite guardada en: {db_path}")
    print(f"[LOAD] Tabla '{TABLE_NAME}' con {len(df):,} registros")
    return conn


# ══════════════════════════════════════════════════════════
# PIPELINE COMPLETO
# ══════════════════════════════════════════════════════════
def run_pipeline() -> tuple[pd.DataFrame, sqlite3.Connection]:
    """Ejecuta Extract → Transform → Load y retorna (df, conn)."""
    print("\n" + "=" * 55)
    print("  PIPELINE ETL — DOCENTES IE PÚBLICAS PERÚ")
    print("=" * 55)
    df_raw   = extract()
    df_clean = transform(df_raw)
    conn     = load(df_clean)
    print("=" * 55)
    print("  PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 55 + "\n")
    return df_clean, conn


if __name__ == "__main__":
    run_pipeline()
