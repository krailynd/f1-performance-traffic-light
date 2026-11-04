import pandas as pd
import numpy as np

def filter_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aísla y remueve outliers por piloto usando el Rango Intercuartílico (IQR).
    En F1, elimina paradas en boxes, vueltas bajo Safety Car y trompos.
    
    Fórmula:
    IQR = Q3 - Q1
    Límite Superior = Q3 + 1.5 * IQR
    Límite Inferior = Q1 - 1.5 * IQR
    """
    clean_parts = []
    for driver, group in df.groupby('driver'):
        q1 = group['lap_time_seconds'].quantile(0.25)
        q3 = group['lap_time_seconds'].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + (1.5 * iqr)
        lower_bound = q1 - (1.5 * iqr)
        
        # Filtrar solo vueltas en el rango representativo
        valid_subset = group[
            (group['lap_time_seconds'] >= lower_bound) & 
            (group['lap_time_seconds'] <= upper_bound)
        ].copy()
        clean_parts.append(valid_subset)
        
    return pd.concat(clean_parts, ignore_index=True) if clean_parts else pd.DataFrame()

def compute_driver_consistency(clean_laps: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas estadísticas de ritmo de carrera y consistencia:
    - Mediana (Medida robusta de ritmo puro, inmune a outliers residuales)
    - Desvío Estándar (Varianza del ritmo del piloto)
    - IQR (Dispersión del 50% central de vueltas)
    """
    stats = clean_laps.groupby('driver').agg(
        clean_laps_count=('lap_time_seconds', 'count'),
        median_time=('lap_time_seconds', 'median'),
        mean_time=('lap_time_seconds', 'mean'),
        std_time=('lap_time_seconds', 'std'),
        iqr_time=('lap_time_seconds', lambda x: x.quantile(0.75) - x.quantile(0.25)),
        best_lap=('lap_time_seconds', 'min')
    ).reset_index()
    
    # Semáforo de consistencia basado en el desvío estándar (std)
    stats['Semáforo_Consistencia'] = stats['std_time'].apply(
        lambda s: '🟢 Alta (Reloj suizo)' if s < 0.45 else ('🟡 Media' if s < 0.85 else '🔴 Baja (Disperso)')
    )
    return stats.sort_values(by='median_time')
