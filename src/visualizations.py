"""
visualizations.py
-----------------
Genera las 8 visualizaciones del análisis de docentes.
Cada función recibe los datos ya preparados (DataFrames o Series)
y guarda la figura en outputs/figures/.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Configuración global ──────────────────────────────────
plt.rcParams["figure.dpi"]    = 150
plt.rcParams["font.family"]   = "DejaVu Sans"
sns.set_theme(style="whitegrid")

PALETTE    = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
FIG_DIR    = "outputs/figures"

os.makedirs(FIG_DIR, exist_ok=True)


def _save(fig: plt.Figure, name: str) -> str:
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [fig] guardada: {path}")
    return path


# ══════════════════════════════════════════════════════════
# FIG 1 · Top 10 departamentos
# ══════════════════════════════════════════════════════════
def fig_top_departamentos(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df["dpto"][::-1], df["total_docentes"][::-1],
                   color=PALETTE[0], edgecolor="white", linewidth=0.5)
    for bar in bars:
        ax.text(bar.get_width() + 300,
                bar.get_y() + bar.get_height() / 2,
                f'{int(bar.get_width()):,}',
                va="center", fontsize=9, color="#374151")
    ax.set_xlabel("Total Docentes", fontsize=11)
    ax.set_title("Top 10 Departamentos por Total de Docentes\n"
                 "(Instituciones Educativas Públicas — Perú)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlim(0, df["total_docentes"].max() * 1.15)
    sns.despine(left=True)
    plt.tight_layout()
    return _save(fig, "01_top_departamentos.png")


# ══════════════════════════════════════════════════════════
# FIG 2 · Distribución por nivel educativo (donut)
# ══════════════════════════════════════════════════════════
def fig_nivel_educativo(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = [PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[4]]
    wedges, _, autotexts = ax.pie(
        df["total_docentes"], labels=None, autopct="%1.1f%%",
        colors=colors, startangle=90,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color("white")
    ax.legend(wedges, df["nivel"], loc="lower center",
              bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=10, frameon=False)
    ax.set_title("Distribución de Docentes\npor Nivel Educativo",
                 fontsize=14, fontweight="bold", pad=20)
    total = df["total_docentes"].sum()
    ax.text(0, 0, f"{total:,}\nDocentes", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#374151")
    plt.tight_layout()
    return _save(fig, "02_nivel_educativo.png")


# ══════════════════════════════════════════════════════════
# FIG 3 · Indicadores urbano vs rural
# ══════════════════════════════════════════════════════════
def fig_urbano_rural(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    w = 0.25
    for i, (col, label, color) in enumerate([
        ("pct_mujeres_promedio",    "% Mujeres",    PALETTE[4]),
        ("pct_nombrados_promedio",  "% Nombrados",  PALETTE[0]),
        ("pct_titulados_promedio",  "% Titulados",  PALETTE[1]),
    ]):
        bars = ax.bar(x + (i - 1) * w, df[col], w,
                      label=label, color=color, alpha=0.85)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.5,
                    f"{bar.get_height():.1f}%",
                    ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(df["area"], fontsize=11)
    ax.set_ylabel("Porcentaje (%)", fontsize=11)
    ax.set_ylim(0, 110)
    ax.set_title("Indicadores Clave por Área (Urbana vs Rural)",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, frameon=False)
    sns.despine()
    plt.tight_layout()
    return _save(fig, "03_urbano_rural.png")


# ══════════════════════════════════════════════════════════
# FIG 4 · Docentes sin título por departamento
# ══════════════════════════════════════════════════════════
def fig_sin_titulo(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [PALETTE[3] if v > 10 else PALETTE[1]
              for v in df["pct_sin_titulo"]]
    ax.bar(df["dpto"], df["pct_sin_titulo"],
           color=colors, edgecolor="white", linewidth=0.5)
    mean_val = df["pct_sin_titulo"].mean()
    ax.axhline(y=mean_val, color="gray", linestyle="--", linewidth=1.2,
               label=f"Promedio: {mean_val:.1f}%")
    for i, (v, d) in enumerate(zip(df["pct_sin_titulo"], df["dpto"])):
        ax.text(i, v + 0.2, f"{v:.1f}%",
                ha="center", va="bottom", fontsize=7.5, rotation=45)
    ax.set_ylabel("% Docentes sin Título", fontsize=11)
    ax.set_title("Top 15 Departamentos con Mayor % de Docentes sin Título",
                 fontsize=13, fontweight="bold")
    ax.set_xticklabels(df["dpto"], rotation=45, ha="right", fontsize=9)
    red_p   = mpatches.Patch(color=PALETTE[3], label="> 10% sin título (crítico)")
    green_p = mpatches.Patch(color=PALETTE[1], label="≤ 10% sin título")
    ax.legend(handles=[red_p, green_p, ax.lines[0]], fontsize=9, frameon=False)
    sns.despine()
    plt.tight_layout()
    return _save(fig, "04_sin_titulo.png")


# ══════════════════════════════════════════════════════════
# FIG 5 · Pirámide etaria
# ══════════════════════════════════════════════════════════
def fig_piramide_etaria(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(9, 5))
    bar_colors = [PALETTE[1], PALETTE[0], PALETTE[2],
                  PALETTE[3], PALETTE[4], "#94A3B8"]
    bars = ax.barh(df["grupo_edad"], df["total_docentes"],
                   color=bar_colors, edgecolor="white", linewidth=0.5)
    for bar in bars:
        ax.text(bar.get_width() + 200,
                bar.get_y() + bar.get_height() / 2,
                f'{int(bar.get_width()):,}',
                va="center", fontsize=9)
    ax.set_xlabel("Número de Docentes", fontsize=11)
    ax.set_title("Distribución Etaria de Docentes a Nivel Nacional",
                 fontsize=13, fontweight="bold")
    ax.set_xlim(0, df["total_docentes"].max() * 1.15)
    sns.despine(left=True)
    plt.tight_layout()
    return _save(fig, "05_piramide_etaria.png")


# ══════════════════════════════════════════════════════════
# FIG 6 · Heatmap de correlación
# ══════════════════════════════════════════════════════════
def fig_correlacion(df_clean: pd.DataFrame) -> str:
    num_cols = ["Docentes_total", "pct_mujeres", "pct_nombrados",
                "pct_con_titulo", "Docentes_25_menos_años",
                "Docentes_3645_años", "Docentes_5665_años"]
    corr = df_clean[num_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    labels = ["Total Docentes", "% Mujeres", "% Nombrados", "% Titulados",
              "Docentes <=25", "Docentes 36-45", "Docentes 56-65"]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, ax=ax,
                linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title("Mapa de Correlación entre Variables Numéricas",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(labels, rotation=0, fontsize=9)
    plt.tight_layout()
    return _save(fig, "06_correlacion.png")


# ══════════════════════════════════════════════════════════
# FIG 7 · Boxplot nivel × área
# ══════════════════════════════════════════════════════════
def fig_boxplot_nivel_area(df_clean: pd.DataFrame) -> str:
    df_box = df_clean[df_clean["Docentes_total"] <= 50]
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.boxplot(data=df_box, x="nivel_clean", y="Docentes_total",
                hue="area_clean",
                palette={"Urbana": PALETTE[0], "Rural": PALETTE[1]},
                ax=ax, width=0.5, linewidth=1.2, fliersize=3)
    ax.set_xlabel("Nivel Educativo", fontsize=11)
    ax.set_ylabel("Docentes por IE", fontsize=11)
    ax.set_title("Distribución de Docentes por IE según Nivel y Área\n"
                 "(Outliers > 50 excluidos para mejor visualización)",
                 fontsize=12, fontweight="bold")
    ax.legend(title="Área", fontsize=10, frameon=False)
    sns.despine()
    plt.tight_layout()
    return _save(fig, "07_boxplot_nivel_area.png")


# ══════════════════════════════════════════════════════════
# FIG 8 · Scatter tamaño IE vs % titulados
# ══════════════════════════════════════════════════════════
def fig_scatter_titulos(df_clean: pd.DataFrame, seed: int = 42) -> str:
    df_s = (df_clean[df_clean["Docentes_total"] <= 60]
            .sample(5000, random_state=seed))
    colors_s = df_s["area_clean"].map({"Urbana": PALETTE[0], "Rural": PALETTE[1]})
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_s["Docentes_total"], df_s["pct_con_titulo"],
               c=colors_s, alpha=0.35, s=18, edgecolors="none")
    m, b = np.polyfit(df_s["Docentes_total"], df_s["pct_con_titulo"], 1)
    x_line = np.linspace(df_s["Docentes_total"].min(),
                         df_s["Docentes_total"].max(), 100)
    r2 = np.corrcoef(df_s["Docentes_total"], df_s["pct_con_titulo"])[0, 1] ** 2
    ax.plot(x_line, m * x_line + b, color="#374151", linewidth=2,
            linestyle="--", label=f"Tendencia (R²={r2:.3f})")
    p1 = mpatches.Patch(color=PALETTE[0], label="Urbana", alpha=0.7)
    p2 = mpatches.Patch(color=PALETTE[1], label="Rural",  alpha=0.7)
    ax.legend(handles=[p1, p2, ax.lines[0]], fontsize=10, frameon=False)
    ax.set_xlabel("Total Docentes por IE", fontsize=11)
    ax.set_ylabel("% Docentes con Título", fontsize=11)
    ax.set_title("Relación entre Tamaño de IE y % de Docentes Titulados\n"
                 "(Muestra: 5,000 instituciones)",
                 fontsize=13, fontweight="bold")
    sns.despine()
    plt.tight_layout()
    return _save(fig, "08_scatter_titulos.png")


# ══════════════════════════════════════════════════════════
# GENERAR TODAS
# ══════════════════════════════════════════════════════════
def generate_all(df_clean: pd.DataFrame, conn) -> None:
    """Llama a todas las funciones de visualización."""
    import sqlite3
    from src.queries import (top_departamentos, distribucion_por_nivel,
                              indicadores_por_area, ranking_sin_titulo,
                              piramide_etaria_nacional)
    print("\n[VIZ] Generando 8 visualizaciones...")
    fig_top_departamentos(top_departamentos(conn))
    fig_nivel_educativo(distribucion_por_nivel(conn))
    fig_urbano_rural(indicadores_por_area(conn))
    fig_sin_titulo(ranking_sin_titulo(conn))
    fig_piramide_etaria(piramide_etaria_nacional(conn))
    fig_correlacion(df_clean)
    fig_boxplot_nivel_area(df_clean)
    fig_scatter_titulos(df_clean)
    print("[VIZ] Todas las figuras generadas.\n")
