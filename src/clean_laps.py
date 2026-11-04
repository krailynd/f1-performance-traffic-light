import pandas as pd
import numpy as np

def filter_quick_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra vueltas para conservar únicamente vueltas representativas de carrera:
    - Sin entrada/salida de pits.
    - Con estatus de pista normal (sin SC/VSC).
    - Vueltas cronometradas válidas.
    """
    valid_laps = laps.pick_quicklaps().copy()
    
    # Calcular tiempo en segundos
    if 'LapTime' in valid_laps.columns:
        valid_laps['LapTimeSeconds'] = valid_laps['LapTime'].dt.total_seconds()
        
    return valid_laps

def compute_driver_consistency(clean_laps: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas estadísticas de ritmo y consistencia por piloto."""
    stats = clean_laps.groupby('Driver').agg(
        total_laps=('LapTimeSeconds', 'count'),
        median_time=('LapTimeSeconds', 'median'),
        mean_time=('LapTimeSeconds', 'mean'),
        std_time=('LapTimeSeconds', 'std'),
        iqr_time=('LapTimeSeconds', lambda x: x.quantile(0.75) - x.quantile(0.25)),
        best_lap=('LapTimeSeconds', 'min')
    ).reset_index()
    
    # Semáforo de consistencia basado en el desvío estándar (std)
    stats['Consistency_Score'] = stats['std_time'].apply(
        lambda s: '🟢 Alta (Muy consistente)' if s < 0.6 else ('🟡 Media' if s < 1.0 else '🔴 Baja (Disperso)')
    )
    return stats.sort_values(by='median_time')
