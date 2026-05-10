"""
main.py
-------
Punto de entrada del proyecto.
Ejecuta el pipeline completo:
  1. ETL  (Extract → Transform → Load)
  2. SQL  (5 consultas analíticas)
  3. VIZ  (8 visualizaciones)
  4. PDF  (reporte ejecutivo)

Uso:
    python main.py
"""

import sys
import os
import sqlite3

# Asegura que src/ sea encontrado al ejecutar desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from src.etl            import run_pipeline
from src.queries        import (top_departamentos, distribucion_por_nivel,
                                 indicadores_por_area, ranking_sin_titulo,
                                 piramide_etaria_nacional, resumen_nacional)
from src.visualizations import (fig_top_departamentos, fig_nivel_educativo,
                                 fig_urbano_rural, fig_sin_titulo,
                                 fig_piramide_etaria, fig_correlacion,
                                 fig_boxplot_nivel_area, fig_scatter_titulos)


def run_queries(conn: sqlite3.Connection) -> dict:
    """Ejecuta las 5 consultas SQL y retorna los resultados."""
    print("\n── CONSULTAS SQL ─────────────────────────────────────")
    results = {
        "top_dptos"  : top_departamentos(conn),
        "niveles"    : distribucion_por_nivel(conn),
        "areas"      : indicadores_por_area(conn),
        "sin_titulo" : ranking_sin_titulo(conn),
        "etaria"     : piramide_etaria_nacional(conn),
        "resumen"    : resumen_nacional(conn),
    }
    print(f"  → 5 consultas ejecutadas correctamente")
    print("\n  KPIs Nacionales:")
    kpis = results["resumen"].iloc[0]
    print(f"    Total IE       : {int(kpis['total_ie']):,}")
    print(f"    Total Docentes : {int(kpis['total_docentes']):,}")
    print(f"    % Mujeres      : {kpis['pct_mujeres']}%")
    print(f"    % Nombrados    : {kpis['pct_nombrados']}%")
    print(f"    % Titulados    : {kpis['pct_titulados']}%")
    print(f"    % IE Rurales   : {kpis['pct_ie_rurales']}%")
    return results


def run_visualizations(df_clean, results: dict) -> None:
    """Genera las 8 figuras."""
    print("\n── VISUALIZACIONES ───────────────────────────────────")
    fig_top_departamentos(results["top_dptos"])
    fig_nivel_educativo(results["niveles"])
    fig_urbano_rural(results["areas"])
    fig_sin_titulo(results["sin_titulo"])
    fig_piramide_etaria(results["etaria"])
    fig_correlacion(df_clean)
    fig_boxplot_nivel_area(df_clean)
    fig_scatter_titulos(df_clean)
    print("  → 8 visualizaciones guardadas en outputs/figures/")


def main():
    print("\n" + "═" * 55)
    print("  ANÁLISIS DE DOCENTES — IE PÚBLICAS DEL PERÚ")
    print("═" * 55)

    # 1. ETL
    df_clean, conn = run_pipeline()

    # 2. SQL
    results = run_queries(conn)

    # 3. Visualizaciones
    run_visualizations(df_clean, results)

    conn.close()
    print("\n" + "═" * 55)
    print("  PROYECTO COMPLETADO")
    print("  Archivos generados:")
    print("    data/processed/docentes_clean.csv")
    print("    data/processed/docentes.db")
    print("    outputs/figures/  (8 gráficos)")
    print("═" * 55 + "\n")


if __name__ == "__main__":
    main()
