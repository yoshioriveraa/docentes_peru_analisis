"""
queries.py
----------
Consultas SQL analíticas sobre la base de datos generada por el pipeline ETL.
Cada función retorna un DataFrame con los resultados listos para graficar o exportar.
"""

import sqlite3
import pandas as pd


# ══════════════════════════════════════════════════════════
# CONSULTAS
# ══════════════════════════════════════════════════════════

def top_departamentos(conn: sqlite3.Connection, n: int = 10) -> pd.DataFrame:
    """
    Top N departamentos por total de docentes.
    Incluye % promedio de mujeres y titulados.
    """
    query = f"""
        SELECT
            dpto,
            SUM(Docentes_total)          AS total_docentes,
            ROUND(AVG(pct_mujeres), 1)   AS avg_pct_mujeres,
            ROUND(AVG(pct_con_titulo), 1) AS avg_pct_titulados
        FROM docentes
        GROUP BY dpto
        ORDER BY total_docentes DESC
        LIMIT {n}
    """
    return pd.read_sql_query(query, conn)


def distribucion_por_nivel(conn: sqlite3.Connection) -> pd.DataFrame:
    """Número de instituciones y docentes agrupados por nivel educativo."""
    query = """
        SELECT
            nivel_clean                          AS nivel,
            COUNT(*)                             AS n_instituciones,
            SUM(Docentes_total)                  AS total_docentes,
            ROUND(AVG(Docentes_total), 2)        AS promedio_por_ie
        FROM docentes
        GROUP BY nivel_clean
        ORDER BY total_docentes DESC
    """
    return pd.read_sql_query(query, conn)


def indicadores_por_area(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Comparación de indicadores clave entre área urbana y rural:
    % mujeres, % nombrados, % titulados.
    """
    query = """
        SELECT
            area_clean                               AS area,
            ROUND(AVG(pct_mujeres), 2)               AS pct_mujeres_promedio,
            ROUND(AVG(pct_nombrados), 2)             AS pct_nombrados_promedio,
            ROUND(AVG(pct_con_titulo), 2)            AS pct_titulados_promedio
        FROM docentes
        GROUP BY area_clean
    """
    return pd.read_sql_query(query, conn)


def ranking_sin_titulo(conn: sqlite3.Connection, n: int = 15) -> pd.DataFrame:
    """
    Ranking de departamentos con mayor porcentaje de docentes sin título.
    """
    query = f"""
        SELECT
            dpto,
            SUM(Docentes_sin_titulo)                         AS sin_titulo,
            SUM(Docentes_total)                              AS total,
            ROUND(100.0 * SUM(Docentes_sin_titulo)
                        / SUM(Docentes_total), 2)            AS pct_sin_titulo
        FROM docentes
        GROUP BY dpto
        ORDER BY pct_sin_titulo DESC
        LIMIT {n}
    """
    return pd.read_sql_query(query, conn)


def piramide_etaria_nacional(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Agregación nacional de los 6 grupos etarios.
    Retorna un DataFrame largo con columnas [grupo, total].
    """
    query = """
        SELECT
            SUM(Docentes_25_menos_años) AS "<=25",
            SUM(Docentes_2635_años)     AS "26-35",
            SUM(Docentes_3645_años)     AS "36-45",
            SUM(Docentes_4655_años)     AS "46-55",
            SUM(Docentes_5665_años)     AS "56-65",
            SUM(Docentes_66_a_mas_años) AS ">=66"
        FROM docentes
    """
    df_wide = pd.read_sql_query(query, conn)
    df_long = df_wide.T.reset_index()
    df_long.columns = ["grupo_edad", "total_docentes"]
    return df_long


def resumen_nacional(conn: sqlite3.Connection) -> pd.DataFrame:
    """KPIs nacionales en una sola fila."""
    query = """
        SELECT
            COUNT(*)                                                   AS total_ie,
            SUM(Docentes_total)                                        AS total_docentes,
            ROUND(100.0 * SUM(Docentes_mujeres)    / SUM(Docentes_total), 2) AS pct_mujeres,
            ROUND(100.0 * SUM(Docentes_nombrados)  / SUM(Docentes_total), 2) AS pct_nombrados,
            ROUND(100.0 * SUM(Docentes_con_titulo) / SUM(Docentes_total), 2) AS pct_titulados,
            ROUND(100.0 * SUM(CASE WHEN area_clean = 'Rural' THEN 1 ELSE 0 END)
                        / COUNT(*), 2)                                 AS pct_ie_rurales
        FROM docentes
    """
    return pd.read_sql_query(query, conn)


# ══════════════════════════════════════════════════════════
# EJECUCIÓN DIRECTA (demo)
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    conn = sqlite3.connect("data/processed/docentes.db")

    print("\n── Resumen Nacional ──")
    print(resumen_nacional(conn).T.to_string())

    print("\n── Top 5 Departamentos ──")
    print(top_departamentos(conn, n=5).to_string(index=False))

    print("\n── Por Nivel Educativo ──")
    print(distribucion_por_nivel(conn).to_string(index=False))

    print("\n── Indicadores por Área ──")
    print(indicadores_por_area(conn).to_string(index=False))

    conn.close()
