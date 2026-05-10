# 📊 Análisis de Docentes — Instituciones Educativas Públicas del Perú

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557c)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-4c72b0)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completado-22c55e)
![License](https://img.shields.io/badge/Licencia-MIT-blue)

---

## 📌 Descripción

Proyecto de análisis de datos aplicado al dataset de **docentes de instituciones educativas públicas del Perú**, con más de **66,000 registros** y **405,000 docentes** a nivel nacional. Implementa un pipeline **ETL modular**, consultas analíticas con **SQL sobre SQLite**, y **8 visualizaciones profesionales**.

> Desarrollado como proyecto de portafolio para demostrar habilidades en análisis de datos con Python.

---

## 🎯 Preguntas de Negocio Respondidas

- ¿Qué departamentos concentran más docentes en el Perú?
- ¿Existe brecha de género en el magisterio peruano?
- ¿Hay diferencias en titulación y estabilidad laboral entre zonas urbanas y rurales?
- ¿Cuál es la estructura etaria del cuerpo docente nacional?
- ¿Qué regiones presentan las brechas más críticas de formación docente?

---

## 🗂️ Estructura del Proyecto

```
docentes_peru/
│
├── 📁 data/
│   ├── raw/
│   │   └── docentes_raw.csv          # Dataset original (MINEDU)
│   └── processed/
│       ├── docentes_clean.csv        # Dataset transformado (generado)
│       └── docentes.db               # Base de datos SQLite (generada)
│
├── 📁 notebooks/
│   └── analisis_exploratorio.ipynb   # Notebook interactivo paso a paso
│
├── 📁 src/
│   ├── __init__.py
│   ├── etl.py                        # Pipeline Extract → Transform → Load
│   ├── queries.py                    # Consultas SQL analíticas
│   └── visualizations.py            # 8 funciones de visualización
│
├── 📁 outputs/
│   ├── figures/                      # 8 gráficos generados (PNG)
│   └── reports/
│       └── reporte_docentes.pdf      # Reporte ejecutivo en PDF
│
├── 📁 docs/
│   └── data_dictionary.md            # Diccionario de datos completo
│
├── main.py                           # Punto de entrada del proyecto
├── requirements.txt                  # Dependencias
├── .gitignore
└── README.md
```

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|---|---|
| **Python 3.10+** | Lenguaje principal |
| **Pandas** | Carga, limpieza y transformación de datos |
| **NumPy** | Operaciones numéricas y feature engineering |
| **Matplotlib** | Gráficos de barras, scatter, donut chart |
| **Seaborn** | Heatmap de correlación y boxplots estadísticos |
| **SQLite3** | Base de datos relacional y consultas SQL |
| **Jupyter Notebook** | Exploración interactiva y documentación |
| **ReportLab** | Generación del reporte ejecutivo en PDF |

---

## ⚙️ Pipeline ETL

```
docentes_raw.csv
      │
      ▼
 ┌─────────────┐
 │   EXTRACT   │  → pandas.read_csv() · validación de integridad
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │  TRANSFORM  │  → limpieza de strings · normalización de categorías
 │             │  → feature engineering (5 columnas nuevas)
 │             │  → eliminación de columnas redundantes
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │    LOAD     │  → docentes_clean.csv · docentes.db (SQLite)
 └─────────────┘
```

**Columnas derivadas creadas:**

| Columna | Descripción |
|---|---|
| `pct_mujeres` | % de docentes mujeres por IE |
| `pct_nombrados` | % de docentes en condición nombrada |
| `pct_con_titulo` | % de docentes titulados |
| `ratio_nombrado_contratado` | Ratio estabilidad laboral |
| `grupo_edad_mayor` | Grupo etario predominante en la IE |

---

## 🔍 Consultas SQL

```sql
-- Top 10 departamentos por total de docentes
SELECT dpto, SUM(Docentes_total) AS total,
       ROUND(AVG(pct_mujeres), 1) AS avg_pct_mujeres
FROM docentes GROUP BY dpto ORDER BY total DESC LIMIT 10;

-- Brecha urbana/rural en indicadores clave
SELECT area_clean,
       ROUND(AVG(pct_mujeres), 2)    AS pct_mujeres,
       ROUND(AVG(pct_nombrados), 2)  AS pct_nombrados,
       ROUND(AVG(pct_con_titulo), 2) AS pct_titulados
FROM docentes GROUP BY area_clean;

-- Ranking de departamentos con mayor % docentes sin título
SELECT dpto,
       ROUND(100.0 * SUM(Docentes_sin_titulo) / SUM(Docentes_total), 2) AS pct_sin_titulo
FROM docentes GROUP BY dpto ORDER BY pct_sin_titulo DESC LIMIT 15;
```

---

## 📊 Visualizaciones

| # | Gráfico | Hallazgo |
|---|---|---|
| 1 | Top 10 departamentos | Lima concentra el 25% del total nacional |
| 2 | Distribución por nivel (donut) | Primaria e Inicial = 83% de los docentes |
| 3 | Indicadores urbano vs rural | IE rurales: menor % nombrados y titulados |
| 4 | % sin título por departamento | Loreto y Ucayali superan el 10% |
| 5 | Pirámide etaria | Grupo 36-45 años es el más numeroso |
| 6 | Heatmap de correlación | Tamaño de IE correlaciona con distribución etaria |
| 7 | Boxplot nivel × área | Secundaria urbana: mayor dispersión en tamaño |
| 8 | Scatter tamaño vs % titulados | Leve tendencia positiva (R² = 0.04) |

---

## 💡 Hallazgos Clave

> 🚺 **61.6%** de los docentes son mujeres — feminización marcada del sector.

> 🌿 **77%** de las IE son rurales, con menor estabilidad laboral que las urbanas.

> 🎓 **96.4%** de los docentes tienen título — pero con brechas regionales críticas.

> 📋 **65.8%** son nombrados; el 34.2% son contratados (mayor precariedad).

> 👥 El grupo **36-45 años** es el más numeroso, con riesgo de relevo generacional.

---

## 🚀 Cómo Ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/docentes-peru-analisis.git
cd docentes-peru-analisis

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el pipeline completo
python main.py

# 5. O explorar el notebook interactivo
jupyter notebook notebooks/analisis_exploratorio.ipynb
```

**Outputs generados automáticamente:**
- `data/processed/docentes_clean.csv` — dataset limpio
- `data/processed/docentes.db` — base de datos SQLite
- `outputs/figures/` — 8 gráficos en PNG

---

## 📄 Documentación

- [`docs/data_dictionary.md`](docs/data_dictionary.md) — Diccionario completo de variables originales y derivadas

---

## 👤 Autor

**[Tu Nombre]** — Analista de Datos  
📧 tucorreo@email.com  
🔗 [LinkedIn](https://linkedin.com/in/tu-perfil)  
💼 [Portfolio](https://tu-portfolio.com)

---

## 📜 Licencia

MIT License — Los datos son de dominio público (MINEDU Perú).
