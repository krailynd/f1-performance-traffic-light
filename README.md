# 🏎️ F1 Performance Traffic Light — Análisis Exploratorio, Aislamiento de Outliers y Consistencia de Pilotos

> **Proyecto 1 — Fase 1 (Python / EDA / Estadística Descriptiva)** de la *Ruta Maestra Deep Learning Researcher*.
> Pipeline reproducible para la extracción de telemetría de Fórmula 1 (API Jolpica-F1 / FastF1), detección matemática de anomalías (IQR), cálculo de varianza de ritmo de carrera y generación del **Semáforo de Rendimiento**.

---

## 📌 1. ¿Qué es y qué problema resuelve este proyecto?

En el automovilismo de élite, el tiempo de vuelta más rápido (*Fastest Lap*) suele ser engañoso: puede ser producto de una parada tardía con neumáticos nuevos y poco combustible. Lo que realmente gana campeonatos es el **ritmo de carrera sostenido y la consistencia**.

Sin embargo, los datos crudos de telemetría de un Gran Premio están profundamente "sucios":
1. **Paradas en boxes (Pits):** Agregan entre 20 y 30 segundos a la vuelta.
2. **Safety Car (SC) y Virtual Safety Car (VSC):** Elevan artificialmente los tiempos entre 30 y 50 segundos.
3. **Banderas amarillas y salidas de pista:** Vueltas con errores puntuales que distorsionan el promedio.

### 🎯 Lo que resuelve este sistema
- **Aislamiento sistemático del ruido:** Implementa un filtro estadístico robusto basado en el Rango Intercuartílico ($IQR$) que purga de manera determinista las vueltas no representativas sin alterar la varianza natural del piloto.
- **El Semáforo de Consistencia:** Clasifica a los pilotos en tres niveles objetivos (`🟢 Reloj Suizo`, `🟡 Consistencia Media`, `🔴 Ritmo Disperso`) usando el desvío estándar ($\sigma$) y la mediana de sus tiempos limpios.
- **Visualización Científica:** Genera *Violin Plots* de alta densidad para comparar no solo la mediana, sino la densidad de probabilidad y los cuartiles de cada competidor.

---

## 📐 2. Fundamentos Matemáticos y Estadísticos Aplicados

### A. Mediana ($\tilde{x}$) vs Media ($\mu$)
La media aritmética es altamente sensible a valores extremos: una sola vuelta bajo Safety Car (ej. 125s vs 86s habitual) desplaza la media hacia arriba.
Por tanto, el ritmo base del piloto se modela mediante la **Mediana**:
$$\tilde{x} = \begin{cases} x_{\frac{n+1}{2}} & \text{si } n \text{ es impar} \\ \frac{1}{2}\left(x_{\frac{n}{2}} + x_{\frac{n}{2} + 1}\right) & \text{si } n \text{ es par} \end{cases}$$

### B. Detección y Filtrado de Outliers por Rango Intercuartílico (IQR)
Para cada piloto $d$, se calculan los cuartiles $Q_1$ (percentil 25) y $Q_3$ (percentil 75):
$$IQR = Q_3 - Q_1$$
Se definen las barreras de Tukey:
$$\text{Límite Inferior} = Q_1 - 1.5 \times IQR$$
$$\text{Límite Superior} = Q_3 + 1.5 \times IQR$$
Cualquier vuelta con $t_{\text{lap}} > \text{Límite Superior}$ (pits, banderas amarillas, incidentes) queda purgada del análisis de ritmo puro.

### C. Desvío Estándar ($\sigma$) como Métrica de Consistencia
La consistencia es inversamente proporcional a la dispersión muestral de las vueltas limpias:
$$\sigma = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (x_i - \bar{x})^2}$$
- **🟢 Alta (Reloj suizo):** $\sigma < 0.45\text{s}$ (el piloto clava sus tiempos décima a décima).
- **🟡 Media:** $0.45\text{s} \le \sigma < 0.85\text{s}$ (degradación normal o gestión de tráfico).
- **🔴 Baja:** $\sigma \ge 0.85\text{s}$ (alta irregularidad o problemas mecánicos).

---

## 🧱 3. Estructura del Repositorio

```text
f1-performance-traffic-light/
├── data/
│   └── cache/             # Vueltas descargadas cacheadas en Apache Parquet
├── reports/
│   └── figures/
│       └── consistency_violin.png  # Gráfico final de alta resolución (300 DPI)
├── src/
│   ├── __init__.py
│   ├── data_loader.py     # Cliente Jolpica-F1 con paginación y caché Parquet
│   ├── clean_laps.py      # Filtro IQR por piloto y cálculo del Semáforo
│   └── visualizer.py      # Generador de gráficos de violín temáticos
├── main.py                # Punto de entrada CLI
├── pyproject.toml         # Configuración del paquete y dependencias
├── requirements.txt       # Dependencias exactas
└── .gitignore
```

---

## 🚀 4. Instalación y Ejecución Verificada

### Requisitos:
- Python 3.10+ (probado en CPython 3.12 con `uv`).

```bash
# 1. Clonar el repositorio
git clone https://github.com/krailynd/f1-performance-traffic-light.git
cd f1-performance-traffic-light

# 2. Crear entorno virtual con uv
uv venv --python 3.12 .venv
source .venv/bin/activate

# 3. Instalar dependencias
uv pip install -r requirements.txt

# 4. Ejecutar el análisis para el GP de Monza 2023 (Round 14)
python main.py --year 2023 --round 14
```

### Salida esperada en consola:
```text
🏎️ Cargando datos para F1 2023 Round 14...
✓ Guardado en caché: data/cache/laps_2023_round_14.parquet (955 vueltas registradas)
📊 Total de vueltas crudas cargadas: 955
🧹 Aplicando filtro matemático IQR para aislar outliers de carrera (pits, SC)...
✨ Vueltas limpias representativas: 874 (outliers removidos: 81)

📋 CALCULANDO SEMÁFORO DE CONSISTENCIA Y RITMO:
=====================================================================================
         driver  clean_laps_count  median_time  std_time  iqr_time Semáforo_Consistencia
 max_verstappen                48      86.0220  0.636843   0.90625               🟡 Media
          sainz                48      86.2910  0.546187   0.82750               🟡 Media
          perez                48      86.3435  0.510042   0.78550               🟡 Media
        russell                47      86.4100  0.356345   0.46350  🟢 Alta (Reloj suizo)
          albon                47      86.8930  0.343390   0.42050  🟢 Alta (Reloj suizo)
=====================================================================================

🎨 Generando visualización de violines estadísticos...
✓ Gráfico guardado en: reports/figures/consistency_violin.png
✅ Pipeline ejecutado con éxito.
```

---

## 👤 Autor
- **Krailynd (Elvis)** — [GitHub](https://github.com/krailynd)
- Proyecto desarrollado como parte de la formación integral hacia **Deep Learning Researcher**.
