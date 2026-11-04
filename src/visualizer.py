from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def apply_f1_theme():
    plt.style.use('dark_background')
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#444444'
    plt.rcParams['axes.linewidth'] = 0.8

def plot_consistency_violin(clean_laps: pd.DataFrame, output_path: str = "reports/figures/consistency_violin.png"):
    """Genera un Violin Plot comparativo de distribución y consistencia de tiempos de vuelta."""
    apply_f1_theme()
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    
    order = list(clean_laps.groupby('driver')['lap_time_seconds'].median().sort_values().index)
    
    sns.violinplot(
        data=clean_laps,
        x='driver',
        y='lap_time_seconds',
        hue='driver',
        order=order,
        inner='quartile',
        palette='magma',
        legend=False,
        cut=0,
        ax=ax
    )
    
    ax.set_title("🏎️ F1 Performance Traffic Light — Ritmo y Consistencia de Pilotos", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Piloto", fontsize=11, labelpad=10)
    ax.set_ylabel("Tiempo de Vuelta Limpio (Segundos)", fontsize=11, labelpad=10)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.25)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✓ Gráfico guardado en: {output_path}")
