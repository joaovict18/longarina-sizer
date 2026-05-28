"""
Gerador de Relatório Visual com Gráficos
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

df = pd.read_csv("resultado_longarina.csv")

# Criar figura com subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise Estrutural de Longarinas - Dimensionador', fontsize=16, fontweight='bold')

# Cores para cada espessura
espessuras = sorted(df['Thickness'].unique())
cores = plt.cm.viridis(np.linspace(0, 1, len(espessuras)))
color_map = {e: cores[i] for i, e in enumerate(espessuras)}

# ========== Gráfico 1: FS vs Posição ==========
ax1 = axes[0, 0]
for espessura in espessuras:
    subset = df[df['Thickness'] == espessura].sort_values('Y')
    label = f"{espessura*1000:.0f}mm"
    ax1.plot(subset['Y'], subset['Safety Factor'], 
             marker='o', markersize=4, linewidth=2, 
             label=label, color=color_map[espessura], alpha=0.8)

ax1.axhline(y=1.5, color='red', linestyle='--', linewidth=2, label='Limite mínimo (1.5)')
ax1.fill_between(df['Y'].unique(), 1.5, 2.5, alpha=0.1, color='green', label='Zona viável')
ax1.set_xlabel('Posição na Envergadura (m)', fontweight='bold')
ax1.set_ylabel('Fator de Segurança (FS)', fontweight='bold')
ax1.set_title('Fator de Segurança ao longo da envergadura', fontweight='bold')
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3)

# ========== Gráfico 2: Tensão vs Posição ==========
ax2 = axes[0, 1]
for espessura in espessuras:
    subset = df[df['Thickness'] == espessura].sort_values('Y')
    label = f"{espessura*1000:.0f}mm"
    ax2.plot(subset['Y'], subset['Sigma']/1e6, 
             marker='s', markersize=4, linewidth=2,
             label=label, color=color_map[espessura], alpha=0.8)

ax2.axhline(y=15, color='red', linestyle='--', linewidth=2, label='σ_adm (15 MPa)')
ax2.set_xlabel('Posição na Envergadura (m)', fontweight='bold')
ax2.set_ylabel('Tensão de Flexão (MPa)', fontweight='bold')
ax2.set_title('Tensão de Flexão ao longo da envergadura', fontweight='bold')
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)

# ========== Gráfico 3: Deflexão vs Posição ==========
ax3 = axes[1, 0]
for espessura in espessuras:
    subset = df[df['Thickness'] == espessura].sort_values('Y')
    label = f"{espessura*1000:.0f}mm"
    ax3.plot(subset['Y'], subset['Deflection']*1000, 
             marker='^', markersize=4, linewidth=2,
             label=label, color=color_map[espessura], alpha=0.8)

ax3.set_xlabel('Posição na Envergadura (m)', fontweight='bold')
ax3.set_ylabel('Deflexão (mm)', fontweight='bold')
ax3.set_title('Deflexão acumulada ao longo da envergadura', fontweight='bold')
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3)

# ========== Gráfico 4: Comparação de Massa e Viabilidade ==========
ax4 = axes[1, 1]
summary_data = []
for espessura in espessuras:
    subset = df[df['Thickness'] == espessura]
    massa = subset['Total mass'].iloc[0]
    fs_min = subset['Safety Factor'].min()
    viavel = '✓ Viável' if fs_min >= 1.5 else '✗ Inviável'
    summary_data.append({
        'Espessura': f"{espessura*1000:.0f}mm",
        'Massa (kg)': massa,
        'FS_mín': fs_min,
        'Viável': 'Sim' if fs_min >= 1.5 else 'Não'
    })

summary_df = pd.DataFrame(summary_data)
colors_bar = ['green' if v == 'Sim' else 'red' for v in summary_df['Viável']]
bars = ax4.bar(summary_df['Espessura'], summary_df['Massa (kg)'], color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)

# Adicionar valores nas barras
for bar, fs in zip(bars, summary_df['FS_mín']):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{fs:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

ax4.set_xlabel('Espessura da Seção', fontweight='bold')
ax4.set_ylabel('Massa Total das Asas (kg)', fontweight='bold')
ax4.set_title('Massa vs Espessura (verde=viável, vermelho=inviável)', fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Adicionar legenda
green_patch = mpatches.Patch(color='green', alpha=0.7, label='FS ≥ 1.5 (Viável)')
red_patch = mpatches.Patch(color='red', alpha=0.7, label='FS < 1.5 (Inviável)')
ax4.legend(handles=[green_patch, red_patch], loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig('relatorio_visual.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo como: relatorio_visual.png")

# Imprimir tabela de resumo
print("\n" + "="*80)
print("RESUMO - COMPARAÇÃO DE CONFIGURAÇÕES")
print("="*80)
print(summary_df.to_string(index=False))
print("="*80)

# Identificar melhor configuração
viavel_idx = summary_df[summary_df['Viável'] == 'Sim'].index
if len(viavel_idx) > 0:
    melhor_idx = summary_df.loc[viavel_idx, 'Massa (kg)'].idxmin()
    melhor = summary_df.loc[melhor_idx]
    print(f"\n🏆 MELHOR CONFIGURAÇÃO (mais leve e viável):")
    print(f"   Espessura: {melhor['Espessura']}")
    print(f"   Massa: {melhor['Massa (kg)']:.4f} kg")
    print(f"   FS mínimo: {melhor['FS_mín']:.3f}")
    print(f"   Status: ✓ RECOMENDADO\n")

print("Visualizações geradas:")
print("  └─ relatorio_visual.png: Gráficos de FS, Tensão, Deflexão e Comparação")
