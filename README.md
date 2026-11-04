# 🏎️ F1 Performance Traffic Light — Análisis Exploratorio y Consistencia de Pilotos

> **Proyecto 1 — Fase 1 (Python / EDA)** de la *Ruta Maestra Deep Learning Researcher*.
> Aplicación de análisis exploratorio de datos (EDA), tratamiento de outliers y estadística descriptiva sobre telemetría de Fórmula 1 usando `FastF1`.

---

## 📌 1. Motivación y Planteamiento del Problema

En las carreras de Fórmula 1, un tiempo de vuelta (*lap time*) está sujeto a una inmensa variabilidad:
- Cargas variables de combustible (efecto de peso a lo largo del stint).
- Degradación térmica y mecánica del compuesto de neumático (*Soft*, *Medium*, *Hard*).
- Interrupciones de carrera (períodos de *Safety Car*, *Virtual Safety Car*, banderas amarillas).
- Tráfico en pista y paradas en boxes (*In-laps*, *Out-laps*).

### 🎯 Objetivo Científico
Desarrollar un pipeline analítico reproducible para:
1. Extraer datos oficiales de telemetría y tiempos de vuelta de un Gran Premio específico.
2. Identificar y aislar sistemáticamente los outliers de carrera (datos atípicos no representativos del ritmo puro).
3. Cuantificar la **consistencia** y el **ritmo de carrera** de cada piloto y constructor mediante visualizaciones estadísticas avanzadas (*Violin plots*, *Box plots* y distribuciones acumuladas).
4. Generar el **Semáforo de Rendimiento**: clasificación objetiva de consistencia (`Baja varianza` vs `Alta dispersión`).

---

## 🧱 2. Estructura del Repositorio

```text
f1-performance-traffic-light/
├── data/                  # Cache local para FastF1 (ignorado por Git)
├── notebooks/             # Cuadernos interactivos para exploración rápida
│   └── 01_exploracion_inicial.ipynb
├── reports/               # Gráficos y reportes generados
│   └── figures/
├── src/                   # Código modular limpio y reutilizable
│   ├── __init__.py
│   ├── data_loader.py     # Carga y caché de sesiones con FastF1
│   ├── clean_laps.py      # Filtro de vueltas válidas y aislamiento de outliers
│   └── visualizer.py      # Generación de gráficos estadísticos (Violin, Boxplots)
├── main.py                # Script CLI ejecutable principal
├── pyproject.toml         # Configuración del entorno Python (uv / pip)
├── requirements.txt       # Dependencias exactas
└── .gitignore             # Reglas para Git (excluye cache y datos pesados)
```

---

## 🛠️ 3. Tecnologías y Librerías

- **Python 3.10+** (gestión recomendada con `uv`)
- **[FastF1](https://docs.fastf1.dev/):** Extracción de timing oficial y telemetría de la FIA.
- **Pandas & NumPy:** Limpieza matricial, cálculo de cuantiles y filtrado condicional.
- **Matplotlib & Seaborn:** Visualizaciones científicas de alta calidad (estilo telemetría oscura).

---

## 🚀 4. Instalación y Ejecución Rápida

### Opción A: Con `uv` (Recomendado)
```bash
git clone https://github.com/krailynd/f1-performance-traffic-light.git
cd f1-performance-traffic-light

# Crear entorno virtual e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Opción B: Con `pip` estándar
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar el análisis:
```bash
# Analizar el GP de Monza 2023 por defecto
python main.py

# O especificar temporada y Gran Premio
python main.py --year 2024 --gp "Bahrain"
```

Los gráficos generados se guardarán automáticamente en `reports/figures/`.

---

## 🔬 5. Metodología de Detección de Outliers (Fórmula 1 ↔ Machine Learning)

En este proyecto se explora cómo el dominio de negocio (F1) define qué es un dato erróneo vs qué es un dato extremo pero legítimo:

| Evento en Pista | Impacto en Telemetría | Tratamiento en el Pipeline |
| :--- | :--- | :--- |
| **Safety Car (SC / VSC)** | Vuelta entre 15s y 40s más lenta que el promedio. | Filtrado por estado de pista (`TrackStatus == '1'`). |
| **Pit In-lap / Out-lap** | Tiempo inflado por paso en pit lane. | Filtrado con `PitInTime.isna()` y `PitOutTime.isna()`. |
| **Banderas Amarillas / Error de piloto** | Salida de pista o pérdida momentánea. | Aislado mediante el rango intercuartílico ($1.5 \times \text{IQR}$). |
| **Stint con Neumático Blando** | Mayor degradación por vuelta. | Segmentación por compuesto para evitar mezcla de distribuciones. |

---

## 👤 Autor
- **Krailynd (Elvis)** — [GitHub](https://github.com/krailynd)
- Proyecto desarrollado como parte de la formación integral hacia **Deep Learning Researcher**.
