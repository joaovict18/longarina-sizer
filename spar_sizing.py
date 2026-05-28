from sections import SectionCircular, SectionRectangular
from spar_segment import SparSegment
import numpy as np
import pandas as pd
import math, json

# Carrega dados de momento fletor ao longo da envergadura
df = pd.read_excel("DIMENSIONAMENTO LONGARINA - SUPERIOR.xlsx")
df = df.iloc[:35]

# Define classe para representar um material com suas propriedades
class Material:
    def __init__(self, nome: str, E: float, sigma_adm: float, rho: float):
        self.nome = nome
        self.E = E                
        self.sigma_adm = sigma_adm 
        self.rho = rho  

# Define classe para representar uma geometria de seção
class GeometriaSecao:
    def __init__(self, tipo: str, base: float = 0.0, altura: float = 0.0, 
                 diametro_ext: float = 0.0, espessura: float = 0.0, comprimento: float = 0.0):
        self.tipo = tipo              
        self.base = base
        self.altura = altura
        self.diametro_ext = diametro_ext
        self.espessura = espessura
        self.comprimento = comprimento


# Instancia materiais com propriedades estruturais
BALSA = Material("Balsa", 3e9, 15e6, 200.0)
FIBRA_CARBONO = Material("Fibra de Carbono", 230e9, 650e6, 1750.0)

# Cria configurações retangulares (Balsa) e circulares (Fibra de Carbono)
sectionsRetangular = []
sectionsCircular = []

for espessura in np.arange(0.001, 0.006, 0.001):
    # Configuração retangular com Balsa
    segments = [
        SparSegment(
            y_start=0.0,
            y_end=0.3,
            section=SectionRectangular(base=0.06, altura=0.032, espessura=espessura, material=BALSA)
        ),
        SparSegment(
            y_start=0.3,
            y_end=0.7,
            section=SectionRectangular(base=0.048, altura=0.02, espessura=espessura, material=BALSA)
        ),
        SparSegment(
            y_start=0.7,
            y_end=1.0,
            section=SectionRectangular(base=0.04, altura=0.01, espessura=espessura, material=BALSA)
        ),
    ]
    sectionsRetangular.append(segments)

    # Configuração circular com Fibra de Carbono
    segments = [
        SparSegment(
            y_start=0.0, 
            y_end=0.3, 
            section=SectionCircular(diametro_ext=0.024, espessura=espessura, material=FIBRA_CARBONO)
        ),
        SparSegment(
            y_start=0.3, 
            y_end=0.7, 
            section=SectionCircular(diametro_ext=0.032, espessura=espessura, material=FIBRA_CARBONO)
        ),
        SparSegment(
            y_start=0.7, 
            y_end=1.0, 
            section=SectionCircular(diametro_ext=0.04, espessura=espessura, material=FIBRA_CARBONO)
        )
    ]
    sectionsCircular.append(segments)


# ========== FUNÇÕES DE CÁLCULO ==========

# Calcula inércia (I) e distância à linha neutra (c) para seções retangulares e circulares
def calculate_inertia_per_section(section):
    results = []

    # SEÇÃO CIRCULAR TUBULAR
    if section.type == "circular":
        externalDiameter = section.diametro_ext
        internalDiameter = (externalDiameter - 2 * section.espessura)
        inertia = (math.pi / 64) * (externalDiameter**4 - internalDiameter**4)
        c = externalDiameter / 2

    # SEÇÃO RETANGULAR
    elif section.type == "retangular":
        minBase = section.base - 2 * section.espessura
        maxBase = section.base
        minAltura = section.altura - 2 * section.espessura
        maxAltura = section.altura
        inertia = ((maxBase * maxAltura**3) / 12 - (minBase * minAltura**3) / 12)
        c = maxAltura / 2

    results.append({
        "Inertia": inertia,
        "DistanceC": c,
        "Thickness": section.espessura
    })

    return results


# Calcula tensão de flexão (sigma = M*c/I)
def calculate_bending_stress(M: float, C: float, I: float):
    sigma = (M * C) / I
    return sigma

# Calcula fator de segurança (FS = sigma_adm / sigma)
def calculate_safety_factor(sigma_adm: float, sigma_max: float):
    return sigma_adm / sigma_max

# Calcula curvatura estrutural (κ = M / EI)
def calculate_structural_curvature(M: float, E: float, I: float):
    return M / (E * I) 

# Integra curvatura para calcular ângulo (θ = ∫κ dy)
def calculate_angle(theta: float, structural_curvature: float, dy: float):
    return theta + structural_curvature * dy

# Integra ângulo para calcular deflexão (v = ∫θ dy)
def calculate_deflection(deflection: float, angle: float, dy: float):
    return deflection + angle * dy


# Calcula massa da estrutura por seção e total
def calculate_mass(configuration):
    total_mass = 0.0
    section_masses = []

    for segment in configuration:
        section = segment.section
        comprimento = segment.y_end - segment.y_start

        # Calcula área dependendo da geometria
        if section.type == "retangular":
            area = ((section.base * section.altura) - (
                (section.base - 2 * section.espessura) * (section.altura - 2 * section.espessura)
                ))
            
        elif section.type == "circular":
            extern_diameter = section.diametro_ext
            intern_diameter = extern_diameter - 2 * section.espessura
            area = (math.pi / 4) * (extern_diameter**2 - intern_diameter**2)

        # Calcula massa: m = ρ * V = ρ * A * L
        volume = area * comprimento
        mass = volume * section.material.rho

        section_masses.append({
            "SectionType": section.type,
            "Length": comprimento,
            "Mass": mass
        })

        total_mass += mass
    
    # Multiplica por 2 para considerar ambas as meias asas
    total_mass *= 2

    return {
        "SectionsMass": section_masses,
        "TotalMass": total_mass
    }


# Função auxiliar: retorna o segmento que contém a posição y
def get_segment(y: float, segments: list):
    for segment in segments:
        if segment.contains(y):
            return segment
    return None


# Executa análise estrutural completa em toda a envergadura
def analyze_span(configuration, df):
    results = []
    theta = 0.0
    deflection = 0.0
    
    mass_data = calculate_mass(configuration=configuration)

    for _, row in df.iterrows():
        y = float(row["Posição y (m)"])
        m = float(row["Momento M (N.m)"])
        dy = float(row["dy (m)"])

        segment = get_segment(y, configuration)

        if segment is None:
            continue

        section = segment.section

        # Calcula propriedades da seção
        inertia_data = calculate_inertia_per_section(section)
        inertia = inertia_data[0]["Inertia"]
        c = inertia_data[0]["DistanceC"]
        thickness = inertia_data[0]["Thickness"]

        # Calcula tensão e fator de segurança
        sigma = calculate_bending_stress(m, c, inertia)
        safety_factor = calculate_safety_factor(section.material.sigma_adm, sigma) 
        
        # Calcula curvatura, ângulo e deflexão
        structural_curvature = calculate_structural_curvature(m, section.material.E, inertia)
        theta = calculate_angle(theta=theta, structural_curvature=structural_curvature, dy=dy)
        deflection = calculate_deflection(deflection=deflection, angle=theta, dy=dy)

        # Armazena resultados
        results.append({
            "Y": y,
            "Inertia": inertia,
            "DistanceC": c,
            "Thickness": thickness,
            "Sigma": sigma,
            "Safety Factor": safety_factor,
            "M/EI": structural_curvature,
            "Angle": theta,
            "Deflection": deflection,
            "Total mass": mass_data["TotalMass"],
            "Mass Per Section": mass_data["SectionsMass"]
        })

    return results


# Função de otimização: encontra a melhor configuração
def otimizar_longarina(sections, material, M):
    melhor_configuracao = None
    melhor_massa = float('inf')
    
    for section in sections:
        I, c = calculate_inertia_per_section([section])
        sigma_max = calculate_bending_stress(M, I[0], c[0])
        fator_seguranca = calculate_safety_factor(material.sigma_adm, sigma_max)
        
        if fator_seguranca >= 1.5:  # Fator de segurança mínimo
            massa = calculate_mass(section, material)
            if massa < melhor_massa:
                melhor_massa = massa
                melhor_configuracao = section

    return melhor_configuracao, melhor_massa


# ========== PROGRAMA PRINCIPAL ==========

if __name__ == "__main__":
    all_results = []

    # Analisa todas as configurações retangulares
    for configuration in sectionsRetangular:
        results = analyze_span(configuration=configuration, df=df)
        all_results.extend(results)

    # Converte dados para formato compatível com CSV
    for result in all_results:
        result["Mass Per Section"] = json.dumps(result["Mass Per Section"])

    # Cria DataFrame e exporta para CSV
    df_results = pd.DataFrame(all_results)
    df_results.to_csv("resultado_longarina.csv", index=False)

    print("✅ CSV exportado com sucesso: resultado_longarina.csv")
