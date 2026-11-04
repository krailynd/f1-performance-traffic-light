import argparse
from src.data_loader import load_race_session
from src.clean_laps import filter_quick_laps, compute_driver_consistency
from src.visualizer import plot_consistency_violin

def main():
    parser = argparse.ArgumentParser(description="F1 Performance Traffic Light Analysis")
    parser.add_argument("--year", type=int, default=2023, help="Temporada de F1 (ej. 2023)")
    parser.add_argument("--gp", type=str, default="Monza", help="Nombre o sede del GP (ej. Monza, Bahrain)")
    args = parser.parse_args()

    print(f"🏎️ Cargando datos para el GP de {args.gp} {args.year}...")
    session = load_race_session(args.year, args.gp)
    
    print("🧹 Filtrando vueltas representativas (aislando outliers y pits)...")
    clean = filter_quick_laps(session.laps)
    
    print("📊 Calculando métricas de consistencia por piloto...")
    stats = compute_driver_consistency(clean)
    print("\n" + "="*70)
    print("📋 TABLA DE CONSISTENCIA Y RITMO DE CARRERA:")
    print("="*70)
    print(stats[['Driver', 'total_laps', 'median_time', 'std_time', 'Consistency_Score']].to_string(index=False))
    
    print("\n🎨 Generando visualizaciones...")
    plot_consistency_violin(clean)
    print("✅ Análisis finalizado con éxito.")

if __name__ == "__main__":
    main()
