"""
Script para identificar qual material está sendo analisado no CSV
"""
import pandas as pd

df = pd.read_csv("resultado_longarina.csv")

print("\n" + "="*80)
print("IDENTIFICANDO MATERIAL DA ANÁLISE")
print("="*80 + "\n")

# Verificar primeira linha para identificar tipo
primeira_linha = df.iloc[0]

# Método 1: Verificar colunas preenchidas
tem_base_altura = pd.notna(primeira_linha['Base']) and pd.notna(primeira_linha['Altura'])
tem_diametro = pd.notna(primeira_linha['Diametro_Externo'])

print("📋 MÉTODO 1: Verificar Colunas Preenchidas")
print("-" * 80)
print(f"Base preenchida?      {tem_base_altura}")
print(f"Altura preenchida?    {tem_base_altura}")
print(f"Diametro preenchido?  {tem_diametro}")
print()

# Método 2: Verificar na coluna Mass Per Section
import json

print("📋 MÉTODO 2: Verificar JSON em 'Mass Per Section'")
print("-" * 80)
mass_json = primeira_linha['Mass Per Section']
try:
    mass_data = json.loads(mass_json.replace('""', '"'))
    section_type = mass_data[0]['SectionType']
    print(f"Tipo de seção no JSON: {section_type}")
except:
    print("Erro ao ler JSON")
print()

# Resultado final
print("="*80)
print("🎯 RESULTADO:")
print("="*80)

if section_type == "retangular":
    print(f"✅ MATERIAL ANALISADO: BALSA")
    print(f"   Geometria: Retangular (Base × Altura)")
    print(f"   Base: {primeira_linha['Base']:.3f} m")
    print(f"   Altura: {primeira_linha['Altura']:.3f} m")
    print(f"   Propriedades:")
    print(f"   ├─ E = 3 GPa")
    print(f"   ├─ σ_adm = 15 MPa")
    print(f"   ├─ ρ = 200 kg/m³")
    print(f"   └─ Espessura = {primeira_linha['Thickness']:.3f} m")
    
elif section_type == "circular":
    print(f"✅ MATERIAL ANALISADO: FIBRA DE CARBONO")
    print(f"   Geometria: Circular Tubular (tubo)")
    print(f"   Diâmetro Externo: {primeira_linha['Diametro_Externo']:.3f} m")
    print(f"   Propriedades:")
    print(f"   ├─ E = 230 GPa")
    print(f"   ├─ σ_adm = 650 MPa")
    print(f"   ├─ ρ = 1750 kg/m³")
    print(f"   └─ Espessura = {primeira_linha['Thickness']:.3f} m")

print("\n" + "="*80)
print("📊 FORMA RÁPIDA DE VERIFICAR NO PANDAS:")
print("="*80)
print("""
# Opção 1: Olhar para colunas
df.iloc[0][['Base', 'Altura', 'Diametro_Externo']]

# Opção 2: Verificar tipo de seção
import json
mass_json = df.iloc[0]['Mass Per Section']
mass_data = json.loads(mass_json.replace('""', '"'))
print(mass_data[0]['SectionType'])  # 'retangular' ou 'circular'

# Opção 3: Checar Material pela Massa
massa = df.iloc[0]['Total mass']
if massa < 0.1:
    print("Provavelmente BALSA (menor densidade)")
else:
    print("Provavelmente FIBRA CARBONO (maior densidade)")
""")
print("="*80 + "\n")
