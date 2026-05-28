## 🔧 COMO ESCOLHER ENTRE BALSA E FIBRA CARBONO

### 📍 Onde está o controle?

No arquivo `spar_sizing.py`, **linha ~270**, procure por:

```python
MATERIAL_SELECIONADO = "balsa"  # ← MUDE AQUI
```

### 🎯 Como mudar?

**Para analisar BALSA (padrão - retangular):**
```python
MATERIAL_SELECIONADO = "balsa"
```
- ✅ Seção: Retangular (Base × Altura)
- ✅ E = 3 GPa
- ✅ σ_adm = 15 MPa
- ✅ ρ = 200 kg/m³

**Para analisar FIBRA DE CARBONO (circular/tubular):**
```python
MATERIAL_SELECIONADO = "fibra_carbono"
```
- ✅ Seção: Circular Tubular
- ✅ E = 230 GPa  
- ✅ σ_adm = 650 MPa
- ✅ ρ = 1750 kg/m³

### 📊 Como verificar qual está sendo analisado?

**Opção 1: Executar e ver a mensagem**
```bash
python spar_sizing.py
# Mensagem mostra:
# 🔍 Analisando BALSA (seção retangular)...
# ou
# 🔍 Analisando FIBRA DE CARBONO (seção circular/tubular)...
```

**Opção 2: Verificar no CSV gerado**
```python
import pandas as pd
df = pd.read_csv("resultado_longarina.csv")

# BALSA: tem Base e Altura preenchidos
df[['Base', 'Altura', 'Diametro_Externo']].iloc[0]

# Resultado BALSA:
# Base: 0.06
# Altura: 0.032
# Diametro: NaN (vazio)

# Resultado FIBRA:
# Base: NaN
# Altura: NaN
# Diametro: 0.024
```

**Opção 3: Verificar JSON em Mass Per Section**
```python
import json
df = pd.read_csv("resultado_longarina.csv")
mass_json = df.iloc[0]['Mass Per Section']
data = json.loads(mass_json.replace('""', '"'))
print(data[0]['SectionType'])  # Mostra: "retangular" ou "circular"
```

### ⚡ Exemplo Prático

**Alterar para Fibra Carbono:**

```bash
# 1. Abrir editor
nano spar_sizing.py

# 2. Encontrar linha ~270 com:
MATERIAL_SELECIONADO = "balsa"

# 3. Mudar para:
MATERIAL_SELECIONADO = "fibra_carbono"

# 4. Salvar (Ctrl+X → Y → Enter)

# 5. Executar
python spar_sizing.py

# 6. Verificar resultado
head -2 resultado_longarina.csv
```

### 📋 Checklist

- [ ] Linha 269-270: `MATERIAL_SELECIONADO = "balsa"` ou `"fibra_carbono"`
- [ ] Executar: `python spar_sizing.py`
- [ ] Verificar mensagem: "Analisando BALSA..." ou "...FIBRA DE CARBONO..."
- [ ] Ver CSV: `head -2 resultado_longarina.csv`
- [ ] Confirmar: Base/Altura preenchidos (BALSA) ou Diametro preenchido (FIBRA)

### 🚀 Velocidade

Mudar material = **1 linha de código** + executar programa
Tempo total: ~5 segundos
