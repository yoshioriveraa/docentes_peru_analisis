# 📖 Diccionario de Datos

Dataset: **Docentes por Institución Educativa Pública — Perú**  
Fuente: Ministerio de Educación del Perú (MINEDU)  
Última actualización del análisis: 2025

---

## Archivo fuente: `data/raw/docentes_raw.csv`

| Columna | Tipo | Descripción |
|---|---|---|
| `cod_mod` | int | Código modular de la IE |
| `anexo` | int | Número de anexo |
| `dir_cen` | str | Nombre o código del centro educativo |
| `niv_mod` | str | Nivel y modalidad (codificado) |
| `nivel` | str | Nivel educativo (ej: `2.Primaria`) |
| `nivel2` | str | Nivel alternativo de clasificación |
| `nivel3` | str | Tercer nivel de clasificación |
| `ges_dep` | str | Gestión y dependencia |
| `gestion` | str | Tipo de gestión (`1.Pública`) |
| `area_censo` | int | Código de área para censo |
| `area` | str | Área geográfica (`1.Urbana` / `2.Rural`) |
| `region` | int | Código numérico de región |
| `dpto` | str | Nombre del departamento |
| `prov` | str | Nombre de la provincia |
| `dist` | str | Nombre del distrito |
| `dre_ugel` | str | DRE o UGEL responsable |
| `region_e` | str | Nombre de la región educativa |
| `Docentes_hombres` | int | Docentes hombres |
| `Docentes_mujeres` | int | Docentes mujeres |
| `Docentes_nombrados` | int | Docentes en condición nombrada |
| `Docentes_contratados` | int | Docentes contratados |
| `Docentes_25_menos_años` | int | Docentes con 25 años o menos |
| `Docentes_2635_años` | int | Docentes entre 26 y 35 años |
| `Docentes_3645_años` | int | Docentes entre 36 y 45 años |
| `Docentes_4655_años` | int | Docentes entre 46 y 55 años |
| `Docentes_5665_años` | int | Docentes entre 56 y 65 años |
| `Docentes_66_a_mas_años` | int | Docentes de 66 años o más |
| `Docentes_con_titulo` | int | Docentes con título profesional |
| `Docentes_sin_titulo` | int | Docentes sin título profesional |
| `Docentes_total` | int | Total de docentes en la IE |

---

## Columnas derivadas (generadas en ETL)

| Columna | Fórmula | Descripción |
|---|---|---|
| `nivel_clean` | `nivel` sin prefijo numérico | Nivel educativo normalizado |
| `area_clean` | `area` sin prefijo numérico | Área normalizada (`Urbana` / `Rural`) |
| `pct_mujeres` | `Docentes_mujeres / Docentes_total × 100` | % docentes mujeres |
| `pct_nombrados` | `Docentes_nombrados / Docentes_total × 100` | % docentes nombrados |
| `pct_con_titulo` | `Docentes_con_titulo / Docentes_total × 100` | % docentes titulados |
| `pct_sin_titulo` | `Docentes_sin_titulo / Docentes_total × 100` | % docentes sin título |
| `ratio_nombrado_contratado` | `Docentes_nombrados / Docentes_contratados` | Ratio estabilidad laboral |
| `grupo_edad_mayor` | `argmax(grupos etarios)` | Grupo etario predominante en la IE |

---

## Notas de Calidad

- El dataset original no presenta valores nulos (0 en las 34 columnas).
- Todos los registros corresponden a gestión pública (`1.Pública`).
- Los códigos internos (`cod_mod`, `codlocal`, etc.) se eliminan en la capa Transform por ser redundantes para el análisis.
- Los grupos etarios suman exactamente `Docentes_total` en todos los registros.
