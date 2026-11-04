import argparse
from src.data_loader import fetch_laps_jolpica, generate_synthetic_benchmark_laps
from src.clean_laps import filter_outliers_iqr, compute_driver_consistency
from src.visualizer import plot_consistency_violin

def main():
    parser = argparse.ArgumentParser(description="F1 Performance Traffic Light Analysis")
    parser.add_argument("--year", type=int, default=2023, help="Temporada de F1 (ej. 2023)")
    parser.add_argument("--round", type=int, default=14, help="Número de Gran Premio (ej. 14 = Monza)")
    args = parser.parse_args()

    print(f"🏎️ Cargando datos para F1 {args.year} Round {args.round}...")
    laps_df = fetch_laps_jolpica(args.year, args.round)
    
    if laps_df.empty:
        print("⚠️ No se pudo obtener datos en vivo; generando benchmark sintético calibrado...")
        laps_df = generate_synthetic_benchmark_laps(50)
        
    print(f"📊 Total de vueltas crudas cargadas: {len(laps_df)}")
    
    print("🧹 Aplicando filtro matemático IQR para aislar outliers de carrera (pits, SC)...")
    clean = filter_outliers_iqr(laps_df)
    print(f"✨ Vueltas limpias representativas: {len(clean)} (outliers removidos: {len(laps_df) - len(clean)})")
    
    print("\n📋 CALCULANDO SEMÁFORO DE CONSISTENCIA Y RITMO:")
    stats = compute_driver_consistency(clean)
    print("=" * 85)
    print(stats[['driver', 'clean_laps_count', 'median_time', 'std_time', 'iqr_time', 'Semáforo_Consistencia']].to_string(index=False))
    print("=" * 85)
    
    print("\n🎨 Generando visualización de violines estadísticos...")
    plot_consistency_violin(clean)
    print("✅ Pipeline ejecutado con éxito.")

if __name__ == "__main__":
    main()
