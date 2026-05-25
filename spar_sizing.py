from sections import SectionCircular, SectionRectangular
import numpy as np
import math


class Material:
    def __init__(self, nome: str, E: float, sigma_adm: float, rho: float):
        self.nome = nome
        self.E = E                
        self.sigma_adm = sigma_adm 
        self.rho = rho  

class GeometriaSecao:
    def __init__(self, tipo: str, base: float = 0.0, altura: float = 0.0, 
                 diametro_ext: float = 0.0, espessura: float = 0.0, comprimento: float = 0.0):
        self.tipo = tipo              
        self.base = base
        self.altura = altura
        self.diametro_ext = diametro_ext
        self.espessura = espessura
        self.comprimento = comprimento




sectionsRetangular = []

for espessura in np.arange(0.001, 0.006, 0.001):
    sections = [
        SectionRectangular(base=0.06, altura=0.032, espessura=espessura),
        SectionRectangular(base=0.048, altura=0.02, espessura=espessura),
        SectionRectangular(base=0.04, altura=0.01, espessura=espessura),
    ]

    sectionsRetangular.append(sections)


sectionsCircular = [
    SectionCircular(diametro_ext=0.024, espessura=0.001), 
    SectionCircular(diametro_ext=0.032, espessura=0.001), 
    SectionCircular(diametro_ext=0.04, espessura=0.001),
]

BALSA = Material("Balsa", 2e9, 15e6, 200.0)
FIBRA_CARBONO = Material("Fibra de Carbono", 230e9, 650e6, 1750.0)


# CALCULAR INÉRCIA E DISTÂNCIA À LINHA NEUTRA PARA CADA TIPO DE SEÇÃO

def calculate_inertia_per_section(list_of_sections: list):

    maxBase = list_of_sections[0].base
    maxAltura = list_of_sections[0].altura
    minBase = list_of_sections[0].base - 2 * list_of_sections[0].espessura
    minAltura = list_of_sections[0].altura - 2 * list_of_sections[0].espessura

    inertia = maxBase * maxAltura**3 / 12 - minBase * minAltura**3 / 12
    c = maxAltura / 2
    return inertia, c


# CALCULAR MASSA POR SEÇÃO COM BASE NA GEOMETRIA E MATERIAL

def calcular_massa_por_secao(geom: GeometriaSecao, material: Material):
    if geom.tipo == "retangular":
        area = geom.base * geom.altura
    elif geom.tipo == "circular":
        area = math.pi * (geom.diametro_ext**2 - (geom.diametro_ext - 2*geom.espessura)**2) / 4
    else:
        raise ValueError("Tipo de seção não suportado")
    
    volume = area * geom.comprimento
    massa = volume * material.rho
    return massa

def calcular_massa_total(sections, material):
    massa_total = 0
    for section in sections:
        massa_total += calcular_massa_por_secao(section, material)
    return massa_total

# AVALIAR A CONFIGURAÇÃO COM BASE NOS REQUISITOS DE ESPAÇO, TENSÃO, FATOR DE SEGURANÇA E MASSA

def calcular_tensao_maxima(M: float, I: float, c: float):
    return M * c / I

def calcular_fator_seguranca(sigma_adm: float, sigma_max: float):
    return sigma_adm / sigma_max

def calcular_curvatura_estrutural(M: float, E: float, I: float):
    return M / (E * I) 

def calcular_angulo(curvatura_estrutural: float):
    x = np.linspace(1.61051E-06, 0.57786453, 30)  
    y = np.full_like(x, curvatura_estrutural)
    return np.trapezoid(y, x) 

def calcular_deflexao(angle: float):
    x = np.linspace(0, 0.01799696, 30)
    y = np.full_like(x, angle)
    return np.trapezoid(y, x)


# OTIMIZAÇÃO DA LONGARINA
def otimizar_longarina(sections, material, M):
    melhor_configuracao = None
    melhor_massa = float('inf')
    
    for section in sections:
        I, c = calculate_inertia_per_section([section])
        sigma_max = calcular_tensao_maxima(M, I[0], c[0])
        fator_seguranca = calcular_fator_seguranca(material.sigma_adm, sigma_max)
        
        if fator_seguranca >= 1.5:  # Fator de segurança mínimo
            massa = calcular_massa_por_secao(section, material)
            if massa < melhor_massa:
                melhor_massa = massa
                melhor_configuracao = section

    return melhor_configuracao, melhor_massa

if __name__ == "__main__":
    print(calculate_inertia_per_section(sectionsRetangular))