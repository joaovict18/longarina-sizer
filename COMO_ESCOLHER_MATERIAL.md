## 🔧 COMO ESCOLHER ENTRE BALSA E FIBRA CARBONO

### 📍 Onde está o controle?

No arquivo `spar_sizing.py`, **linha ~270**, procure por:

```python
MODO_ANALISE = "ambos"  # ← MUDE AQUI
```

### 🎯 Opções de Análise

**1. Analisar apenas BALSA (retangular):**
```python
MODO_ANALISE = "balsa"
```
- Seção: Retangular (Base × Altura)
- E = 3 GPa
- σ_adm = 15 MPa
- ρ = 200 kg/m³
- **Saída**: 175 linhas no CSV (35 pontos × 5 espessuras)

**2. Analisar apenas FIBRA DE CARBONO (circular/tubular):**
```python
MODO_ANALISE = "fibra_carbono"
```
- Seção: Circular Tubular
- E = 230 GPa
- σ_adm = 650 MPa
- ρ = 1750 kg/m³
- **Saída**: 175 linhas no CSV (35 pontos × 5 espessuras)

**3. Analisar AMBOS simultaneamente (RECOMENDADO):**
```python
MODO_ANALISE = "ambos"
```
- Analisa Balsa E Fibra Carbono em uma única execução
- **Saída**: 350 linhas no CSV (175 Balsa + 175 Fibra Carbono)
- Coluna `Material` identifica cada material
- Gráficos de comparação lado a lado (FS, Tensão, Deflexão, Massa)

### 📊 Como Verificar o Resultado

**Opção 1: Pela mensagem ao executar**
```bash
python spar_sizing.py

# Saída mostra:
# 🔍 Modo de análise: AMBOS
# 📊 Analisando BALSA...
# 📊 Analisando FIBRA DE CARBONO...
# 📈 Total: 350 linhas (175 Balsa + 175 Fibra)
```

**Opção 2: Verificar coluna Material no CSV**
```python
import pandas as pd
df = pd.read_csv("resultado_longarina.csv")

# Ver materiais
print(df['Material'].unique())
# Output: ['Balsa', 'Fibra de Carbono']

# Contar linhas por material
print(df['Material'].value_counts())
# Balsa: 175
# Fibra de Carbono: 175
```

**Opção 3: Gráficos de Comparação**
```bash
# Executar para gerar relatorio_visual.png com gráficos comparativos
python gerar_relatorio_visual.py

# Se modo é "ambos", gera 6 gráficos lado a lado:
# ├─ FS: Balsa vs Fibra Carbono
# ├─ Tensão: Balsa vs Fibra Carbono
# ├─ Comparação de Massa
# └─ Resumo de Viabilidade
```

### 💡 Comparação Rápida dos Materiais

| Aspecto | Balsa | Fibra Carbono |
|---------|-------|---------------|
| **Geometria** | Retangular | Circular/Tubular |
| **E (MPa)** | 3,000 | 230,000 |
| **σ_adm (MPa)** | 15 | 650 |
| **ρ (kg/m³)** | 200 | 1,750 |
| **Menor t viável** | 5 mm | 1 mm |
| **Massa (5mm)** | 0.2392 kg | 0.3409 kg |
| **FS (5mm mín)** | 1.557 | 4.239 |

### ⚡ Exemplo Prático - Modo Comparação

```bash
# 1. Editar spar_sizing.py
nano spar_sizing.py
# Encontrar: MODO_ANALISE = "balsa"
# Mudar para: MODO_ANALISE = "ambos"
# Salvar (Ctrl+X → Y → Enter)

# 2. Executar análise
python spar_sizing.py

# Output:
# 🔍 Modo de análise: AMBOS
# 📊 Analisando BALSA (seção retangular)...
# 📊 Analisando FIBRA DE CARBONO (seção circular/tubular)...
# ✅ Análise concluída!
# 📊 CSV exportado: resultado_longarina.csv
#    ├─ BALSA: 175 linhas (35 pontos × 5 espessuras)
#    └─ FIBRA CARBONO: 175 linhas (35 pontos × 5 espessuras)
#    📈 Total: 350 linhas

# 3. Gerar gráficos comparativos
python gerar_relatorio_visual.py

# Output mostra:
# ✅ 2 materiais encontrados - gerando comparação lado a lado!
# ✅ Gráfico salvo como: relatorio_visual.png
# Tabela com resumo de massa por material e espessura
```

### 📋 Checklist Rápido

- [ ] **Modo único** (1 material): mude para `"balsa"` ou `"fibra_carbono"`
- [ ] **Modo comparação** (ambos): deixe em `"ambos"`
- [ ] Executar: `python spar_sizing.py`
- [ ] Gerar gráficos: `python gerar_relatorio_visual.py`
- [ ] CSV gerado: `resultado_longarina.csv` (150 ou 350 linhas)
- [ ] Gráficos: `relatorio_visual.png` (comparativo ou simples)
