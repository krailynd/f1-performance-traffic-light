from pathlib import Path
import fastf1
import pandas as pd

def setup_cache(cache_dir: str = "data/cache"):
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_path))

def load_race_session(year: int, gp: str) -> fastf1.core.Session:
    """Carga una sesión de carrera y sus vueltas."""
    setup_cache()
    session = fastf1.get_session(year, gp, 'R')
    session.load(laps=True, telemetry=False, weather=True)
    return session
