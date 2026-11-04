from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def apply_f1_theme():
    plt.style.use('dark_background')
    plt.rcParams['font.sans-serif'] = 'sans-serif'
    plt.rcParams['axes.edgecolor'] = '#444444'
    plt.rcParams['axes.linewidth'] = 0.8

def plot_consistency_violin(clean_laps: pd.DataFrame, output_path: str = "reports/figures/consistency_violin.png"):
    apply_f1_theme()
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    
    # Ordenar pilotos por tiempo mediano
    order = clean_laps.groupby('Driver')['LapTimeSeconds'].median().sort_values().index
    
    sns.violinplot(
        data=clean_laps,
        x='Driver',
        y='LapTimeSeconds',
        order=order,
        inner='quartile',
        palette='flare',
        cut=0,
        ax=ax
    )
    
    ax.set_title("Distribución y Consistencia de Tiempos de Vuelta (Clean Laps)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Piloto", fontsize=11, labelpad=10)
    ax.set_ylabel("Tiempo de Vuelta (Segundos)", fontsize=11, labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✓ Gráfico guardado en: {output_path}")
