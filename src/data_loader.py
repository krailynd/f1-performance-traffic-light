from pathlib import Path
import time
import requests
import pandas as pd

CACHE_DIR = Path("data/cache")

def parse_time_to_seconds(time_str: str) -> float:
    """Convierte cadenas '1:25.123' a segundos (85.123)."""
    try:
        parts = time_str.split(":")
        if len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        return float(time_str)
    except Exception:
        return None

def fetch_laps_jolpica(season: int = 2023, round_num: int = 14) -> pd.DataFrame:
    """Descarga todas las vueltas de carrera mediante Jolpica-F1 con paginación automática y caché."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"laps_{season}_round_{round_num}.parquet"
    
    if cache_file.exists():
        print(f"📦 Usando caché local: {cache_file}")
        return pd.read_parquet(cache_file)
        
    print(f"🌐 Descargando vueltas de F1 {season} Round {round_num} desde Jolpica-F1...")
    base_url = f"http://api.jolpi.ca/ergast/f1/{season}/{round_num}/laps.json"
    limit = 100
    offset = 0
    all_rows = []
    
    while True:
        url = f"{base_url}?limit={limit}&offset={offset}"
        try:
            resp = requests.get(url, timeout=12)
            if resp.status_code != 200:
                print(f"⚠️ Error {resp.status_code} al consultar {url}")
                break
            data = resp.json()
            races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if not races:
                break
            
            laps = races[0].get("Laps", [])
            if not laps:
                break
                
            for lap_obj in laps:
                lap_num = int(lap_obj.get("number", 0))
                for timing in lap_obj.get("Timings", []):
                    time_raw = timing.get("time")
                    sec = parse_time_to_seconds(time_raw)
                    all_rows.append({
                        "season": season,
                        "round": round_num,
                        "lap_number": lap_num,
                        "driver": timing.get("driverId"),
                        "position": int(timing.get("position", 0)),
                        "time_str": time_raw,
                        "lap_time_seconds": sec
                    })
                    
            total_items = int(data.get("MRData", {}).get("total", 0))
            offset += limit
            if offset >= total_items:
                break
            time.sleep(0.15)
        except Exception as e:
            print(f"⚠️ Error en descarga: {e}")
            break
            
    df = pd.DataFrame(all_rows)
    if not df.empty:
        df.to_parquet(cache_file, index=False)
        print(f"✓ Guardado en caché: {cache_file} ({len(df)} vueltas registradas)")
    return df

def generate_synthetic_benchmark_laps(n_laps: int = 50) -> pd.DataFrame:
    """Genera datos sintéticos de prueba con parámetros reales de F1 (Monza) si no hay red."""
    import numpy as np
    drivers = ['max_verstappen', 'perez', 'sainz', 'leclerc', 'hamilton', 'russell', 'norris', 'albon']
    rows = []
    np.random.seed(42)
    for d in drivers:
        base_time = 84.5 + np.random.uniform(0.1, 1.2)
        variance = 0.35 if 'verstappen' in d or 'sainz' in d else 0.85
        for l in range(1, n_laps + 1):
            time_sec = base_time + (l * 0.05) + np.random.normal(0, variance)
            # Agregar outliers simulados (lap 12 pit, lap 25 SC)
            if l in (12, 30):
                time_sec += 22.0 # Pit stop
            if l in (25, 26):
                time_sec += 35.0 # Safety car
            rows.append({
                "season": 2023,
                "round": 14,
                "lap_number": l,
                "driver": d,
                "position": 1,
                "time_str": f"{int(time_sec//60)}:{time_sec%60:06.3f}",
                "lap_time_seconds": time_sec
            })
    return pd.DataFrame(rows)
