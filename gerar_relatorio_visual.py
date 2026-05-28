"""
Gerador de Relatório Visual Comparativo: Balsa vs Fibra Carbono
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 12)
plt.rcParams['font.size'] = 9

df = pd.read_csv("resultado_longarina.csv")

# Verificar se há comparação possível
materiais = df['Material'].unique()
print(f"\n📊 Materiais encontrados no CSV: {list(materiais)}")

if len(materiais) == 1:
    print(f"⚠️  Apenas 1 material ({materiais[0]}) - gerando relatório simples...")
    modo_comparacao = False
else:
    print(f"✅ 2 materiais encontrados - gerando comparação lado a lado!")
    modo_comparacao = True

# Cores por material
cores_material = {
    "Balsa": "#1f77b4",  # Azul
    "Fibra de Carbono": "#ff7f0e"  # Laranja
}

# Criar figura com subplots
if modo_comparacao:
    fig, axes = plt.subplots(3, 2, figsize=(18, 14))
    fig.suptitle('Comparação: Balsa vs Fibra de Carbono - Análise Estrutural', 
                 fontsize=16, fontweight='bold')
else:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Análise Estrutural - {materiais[0]}', fontsize=16, fontweight='bold')

# ========== MODO COMPARAÇÃO (2 materiais) ==========
if modo_comparacao:
    
    # ========== Gráfico 1: FS vs Posição - BALSA ==========
    ax = axes[0, 0]
    for t in sorted(df['Thickness'].unique()):
        subset = df[(df['Thickness'] == t) & (df['Material'] == 'Balsa')].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Safety Factor'], 
                marker='o', markersize=3, linewidth=2, label=label, alpha=0.8)
    ax.axhline(y=1.5, color='red', linestyle='--', linewidth=2, label='Limite (1.5)')
    ax.fill_between(df['Y'].unique(), 1.5, 2.5, alpha=0.1, color='green')
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('FS', fontweight='bold')
    ax.set_title('BALSA: Fator de Segurança', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # ========== Gráfico 2: FS vs Posição - FIBRA ==========
    ax = axes[0, 1]
    for t in sorted(df['Thickness'].unique()):
        subset = df[(df['Thickness'] == t) & (df['Material'] == 'Fibra de Carbono')].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Safety Factor'], 
                marker='s', markersize=3, linewidth=2, label=label, alpha=0.8)
    ax.axhline(y=1.5, color='red', linestyle='--', linewidth=2, label='Limite (1.5)')
    ax.fill_between(df['Y'].unique(), 1.5, 100, alpha=0.1, color='green')
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('FS', fontweight='bold')
    ax.set_title('FIBRA CARBONO: Fator de Segurança', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=1.0)
    
    # ========== Gráfico 3: Tensão vs Posição - BALSA ==========
    ax = axes[1, 0]
    for t in sorted(df['Thickness'].unique()):
        subset = df[(df['Thickness'] == t) & (df['Material'] == 'Balsa')].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Sigma']/1e6, 
                marker='o', markersize=3, linewidth=2, label=label, alpha=0.8)
    ax.axhline(y=15, color='red', linestyle='--', linewidth=2, label='σ_adm (15 MPa)')
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('Tensão (MPa)', fontweight='bold')
    ax.set_title('BALSA: Tensão de Flexão', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # ========== Gráfico 4: Tensão vs Posição - FIBRA ==========
    ax = axes[1, 1]
    for t in sorted(df['Thickness'].unique()):
        subset = df[(df['Thickness'] == t) & (df['Material'] == 'Fibra de Carbono')].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Sigma']/1e6, 
                marker='s', markersize=3, linewidth=2, label=label, alpha=0.8)
    ax.axhline(y=650, color='red', linestyle='--', linewidth=2, label='σ_adm (650 MPa)')
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('Tensão (MPa)', fontweight='bold')
    ax.set_title('FIBRA CARBONO: Tensão de Flexão', fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # ========== Gráfico 5: Comparação de Massa ==========
    ax = axes[2, 0]
    summary_data = []
    for material in ['Balsa', 'Fibra de Carbono']:
        for espessura in sorted(df['Thickness'].unique()):
            subset = df[(df['Thickness'] == espessura) & (df['Material'] == material)]
            if len(subset) > 0:
                massa = subset['Total mass'].iloc[0]
                fs_min = subset['Safety Factor'].min()
                summary_data.append({
                    'Material': material,
                    'Espessura': f"{espessura*1000:.0f}mm",
                    'Massa': massa,
                    'FS_min': fs_min
                })
    
    summary_df = pd.DataFrame(summary_data)
    
    x = np.arange(len(summary_df['Espessura'].unique()))
    width = 0.35
    
    balsa_massas = summary_df[summary_df['Material'] == 'Balsa']['Massa'].values
    fibra_massas = summary_df[summary_df['Material'] == 'Fibra de Carbono']['Massa'].values
    
    ax.bar(x - width/2, balsa_massas, width, label='Balsa', color=cores_material['Balsa'], alpha=0.8)
    ax.bar(x + width/2, fibra_massas, width, label='Fibra Carbono', color=cores_material['Fibra de Carbono'], alpha=0.8)
    
    ax.set_xlabel('Espessura', fontweight='bold')
    ax.set_ylabel('Massa Total (kg)', fontweight='bold')
    ax.set_title('Comparação de Massa', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(summary_df['Espessura'].unique())
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # ========== Gráfico 6: Resumo de Viabilidade ==========
    ax = axes[2, 1]
    ax.axis('off')
    
    resumo_text = "📊 RESUMO COMPARATIVO\n" + "="*45 + "\n\n"
    
    for material in ['Balsa', 'Fibra de Carbono']:
        subset = df[df['Material'] == material]
        viavel = subset[subset['Safety Factor'] >= 1.5]
        
        if len(viavel) > 0:
            espessuras_viaveis = sorted(viavel['Thickness'].unique())
            melhor_t = espessuras_viaveis[0]
            melhor_subset = subset[subset['Thickness'] == melhor_t]
            melhor_massa = melhor_subset['Total mass'].iloc[0]
            melhor_fs = melhor_subset['Safety Factor'].min()
            
            resumo_text += f"✅ {material.upper()}\n"
            resumo_text += f"   Melhor: {melhor_t*1000:.0f}mm\n"
            resumo_text += f"   Massa: {melhor_massa:.4f} kg\n"
            resumo_text += f"   FS mín: {melhor_fs:.3f}\n\n"
        else:
            resumo_text += f"❌ {material.upper()}\n"
            resumo_text += f"   Nenhuma configuração\n"
            resumo_text += f"   viável (FS < 1.5)\n\n"
    
    ax.text(0.05, 0.95, resumo_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ========== MODO SIMPLES (1 material) ==========
else:
    material = materiais[0]
    
    # Gráfico 1: FS vs Posição
    ax = axes[0, 0]
    for t in sorted(df['Thickness'].unique()):
        subset = df[df['Thickness'] == t].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Safety Factor'], 
                marker='o', markersize=4, linewidth=2, label=label, alpha=0.8)
    ax.axhline(y=1.5, color='red', linestyle='--', linewidth=2, label='Limite')
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('FS', fontweight='bold')
    ax.set_title('Fator de Segurança', fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Gráfico 2: Tensão
    ax = axes[0, 1]
    for t in sorted(df['Thickness'].unique()):
        subset = df[df['Thickness'] == t].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Sigma']/1e6, 
                marker='s', markersize=4, linewidth=2, label=label, alpha=0.8)
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('Tensão (MPa)', fontweight='bold')
    ax.set_title('Tensão de Flexão', fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Gráfico 3: Deflexão
    ax = axes[1, 0]
    for t in sorted(df['Thickness'].unique()):
        subset = df[df['Thickness'] == t].sort_values('Y')
        label = f"{t*1000:.0f}mm"
        ax.plot(subset['Y'], subset['Deflection']*1000, 
                marker='^', markersize=4, linewidth=2, label=label, alpha=0.8)
    ax.set_xlabel('Posição Y (m)', fontweight='bold')
    ax.set_ylabel('Deflexão (mm)', fontweight='bold')
    ax.set_title('Deflexão Acumulada', fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Gráfico 4: Massa
    ax = axes[1, 1]
    summary_data = []
    for espessura in sorted(df['Thickness'].unique()):
        subset = df[df['Thickness'] == espessura]
        massa = subset['Total mass'].iloc[0]
        fs_min = subset['Safety Factor'].min()
        summary_data.append({'Espessura': f"{espessura*1000:.0f}mm", 'Massa': massa, 'FS': fs_min})
    
    summary_df = pd.DataFrame(summary_data)
    colors_bar = ['green' if fs >= 1.5 else 'red' for fs in summary_df['FS']]
    bars = ax.bar(summary_df['Espessura'], summary_df['Massa'], color=colors_bar, alpha=0.7, edgecolor='black')
    
    for bar, fs in zip(bars, summary_df['FS']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{fs:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    ax.set_xlabel('Espessura', fontweight='bold')
    ax.set_ylabel('Massa (kg)', fontweight='bold')
    ax.set_title('Massa vs Espessura', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('relatorio_visual.png', dpi=300, bbox_inches='tight')
print(f"\n✅ Gráfico salvo como: relatorio_visual.png")

if modo_comparacao:
    print("\n" + "="*80)
    print("📊 COMPARAÇÃO - RESUMO MASSA POR MATERIAL E ESPESSURA")
    print("="*80)
    print(summary_df.to_string(index=False))
