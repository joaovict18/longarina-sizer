# Dimensionador de Longarinas - Spar Sizing

## O que é?

Sistema computacional para análise estrutural de longarinas (vigas de reforço) de asas de aeronaves. Calcula propriedades estruturais, tensões, fatores de segurança e massa para diferentes configurações de materiais e espessuras.

---

## Início Rápido

### Instalação
```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Executar
```bash
python spar_sizing.py
```

Saída: `resultado_longarina.csv` (176 linhas com análise de 35 pontos × 5 configurações)

---

## ⚙️ Como Funciona

### 1. **Carregamento de Dados**
Lê momento fletor (M) em 35 pontos da envergadura a partir do Excel:
```
Posição y: 0.022m → 1.0m
Momento M: máximo na raiz, mínimo na ponta
```

### 2. **Configurações Analisadas**
- **5 Balsa retangular:** espessuras 0.001 a 0.005 m
- **5 Fibra circular:** mesmas espessuras

Cada com **3 seções progressivas:**
| Seção | Posição | Base/Diâm | Altura |
|-------|---------|-----------|--------|
| 1 | 0.0-0.3m | 0.060m | 0.032m |
| 2 | 0.3-0.7m | 0.048m | 0.020m |
| 3 | 0.7-1.0m | 0.040m | 0.010m |

### 3. **Cálculos por Ponto**

#### **Inércia (I)**
- Retangular: `I = (B×H³)/12 - (b×h³)/12`
- Circular: `I = (π/64)×(De⁴ - Di⁴)`

#### **Tensão (σ)**
```
σ = (M × c) / I
```
Onde c = distância à linha neutra

#### **Fator de Segurança (FS)**
```
FS = σ_adm / σ
```
**Requisito:** FS ≥ 1.5 (mandatório)

#### **Deflexão**
Integração numérica:
```
κ = M/(E×I)          [curvatura]
θ = ∫κ dy            [ângulo]
v = ∫θ dy            [deflexão]
```

#### **Massa**
```
Area = B×H - b×h (retangular) ou π/4×(De²-Di²) (circular)
Massa = ρ × Area × comprimento × 2
```

---

## Interpretação do CSV

### Colunas Principais

| Coluna | Unidade | Significado | Alerta |
|--------|---------|-------------|--------|
| **Y** | m | Posição na envergadura | - |
| **Thickness** | m | Espessura analisada | 0.001-0.005 |
| **Inertia** | m⁴ | Resistência à flexão | Maior = melhor |
| **Sigma** | Pa | Tensão desenvolvida | Menor = melhor |
| **Safety Factor** | - | Margem de segurança | **≥ 1.5 obrigatório** |
| **Deflection** | m | Deslocamento vertical | Menor = melhor |
| **Total mass** | kg | Peso de ambas asas | Para otimização |

### Exemplo de Leitura

```
Linha 1 (Balsa 1mm, y=0.022m):
├─ Sigma = 29.36 MPa        (tensão alta)
├─ Safety Factor = 0.511     FALHA (< 1.5)
└─ Razão: espessura insuficiente

Linha 176 (Balsa 5mm, y=0.958m):
├─ Sigma = 1.82 MPa         (tensão baixa)
├─ Safety Factor = 8.24      SEGURO (>> 1.5)
└─ Razão: espessura adequada, momento reduzido na ponta
```

### Análise Rápida

```python
import pandas as pd

df = pd.read_csv("resultado_longarina.csv")

# Configurações viáveis (FS ≥ 1.5)
viavel = df[df["Safety Factor"] >= 1.5]
print(f"Linhas válidas: {len(viavel)} de {len(df)}")

# Espessura ótima (mais leve)
for t in df["Thickness"].unique():
    mass = df[df["Thickness"] == t]["Total mass"].iloc[0]
    fs_min = df[df["Thickness"] == t]["Safety Factor"].min()
    valid = "✓" if fs_min >= 1.5 else "✗"
    print(f"{valid} t={t*1000:.0f}mm: Massa={mass:.3f}kg, FS_min={fs_min:.2f}")
```

---

## Estrutura do Projeto

```
├── spar_sizing.py              (código principal)
├── sections.py                 (classes de seção)
├── spar_segment.py             (classes de segmento)
├── resultado_longarina.csv     (saída gerada)
├── EXPLICACAO_FUNCIONAMENTO.md (detalhes técnicos)
└── requirements.txt            (dependências)
```

---

## Materiais Padrão

| Material | E (GPa) | σ_adm (MPa) | ρ (kg/m³) |
|----------|---------|-------------|-----------|
| **Balsa** | 3 | 15 | 200 |
| **Fibra Carbono** | 230 | 650 | 1750 |

---

## Resultados Esperados

✅ Balsa com espessura adequada (~5mm) é **mais leve** que Fibra  
✅ Fator de segurança mínimo ocorre na **raiz da asa** (maior M)  
✅ Deflexão acumula ao longo da envergadura  

---

## Troubleshooting

**Erro: "Excel file not found"**
```bash
# Certifique-se de que o arquivo existe:
ls "DIMENSIONAMENTO LONGARINA - SUPERIOR.xlsx"
```

**CSV vazio ou com poucos dados**
```bash
# Verificar arquivo Excel tem dados na coluna "Posição y (m)"
```

---

## Referência

- **PDF Base:** "Passo a passo: Dimensionamento Estrutural de Longarina feito por Iasmim"
- **Método:** Análise de vigas sob flexão pura
- **Integração:** Método trapezoidal (dy = 0.001m)

---
