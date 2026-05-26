from sections import SectionCircular, SectionRectangular
import numpy as np
import math, json


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
sectionsCircular = []

for espessura in np.arange(0.001, 0.006, 0.001):
    sections = [
        SectionRectangular(base=0.06, altura=0.032, espessura=espessura),
        SectionRectangular(base=0.048, altura=0.02, espessura=espessura),
        SectionRectangular(base=0.04, altura=0.01, espessura=espessura),
    ]

    sectionsRetangular.append(sections)

    sections = [
        SectionCircular(diametro_ext=0.024, espessura=espessura), 
        SectionCircular(diametro_ext=0.032, espessura=espessura), 
        SectionCircular(diametro_ext=0.04, espessura=espessura),
    ]

    sectionsCircular.append(sections)


BALSA = Material("Balsa", 2e9, 15e6, 200.0)
FIBRA_CARBONO = Material("Fibra de Carbono", 230e9, 650e6, 1750.0)


# CALCULAR INÉRCIA E DISTÂNCIA À LINHA NEUTRA PARA CADA TIPO DE SEÇÃO

def calculate_inertia_per_section(list_of_sections: list):

    results = []

    for configuration in list_of_sections:

        total_inertia = 0
        max_c = 0

        section_results = []

        for section in configuration:

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

            section_results.append({

                "Type": section.type,
                "Inertia": inertia,
                "DistanceC": c
            })

            total_inertia += inertia

            if c > max_c:
                max_c = c

        results.append({
            "Inertia": total_inertia,
            "DistanceC": max_c,
            "Thickness": configuration[0].espessura,    
            "Sections Results": section_results
        })

    return results

# CALCULAR MASSA POR SEÇÃO COM BASE NA GEOMETRIA E MATERIAL

def calculate_mass(results: list, configurations: list, material):
    for config_index, config in enumerate(configurations):

        total_mass = 0

        for section_index, section in enumerate(config):
            if section.type == "retangular":
                area = ((section.base * section.altura) - ((section.base - 2 * section.espessura)
                        * (section.altura - 2 * section.espessura)))
                
            elif section.type == "circular":
                d_ext = section.diametro_ext
                d_int = d_ext - 2 * section.espessura

                area = (math.pi / 4) * (d_ext**2 - d_int**2)

            volume = area * section.comprimento
            mass = volume * material.rho

            results[config_index]["Sections Results"][section_index]["Mass"] = float(mass)
            total_mass += mass
            total_mass *= 2

        results[config_index]["TotalMass"] = float(total_mass)

    return results

# AVALIAR A CONFIGURAÇÃO COM BASE NOS REQUISITOS DE ESPAÇO, TENSÃO, FATOR DE SEGURANÇA E MASSA

def calculate_bending_stress(results: list, M: float):
    for config in results:
        for section in config["Sections Results"]:
            sigma = (M * section["DistanceC"]) / section["Inertia"]
            section["Bending Stress"] = sigma

    return results 

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
        sigma_max = calculate_bending_stress(M, I[0], c[0])
        fator_seguranca = calcular_fator_seguranca(material.sigma_adm, sigma_max)
        
        if fator_seguranca >= 1.5:  # Fator de segurança mínimo
            massa = calculate_mass(section, material)
            if massa < melhor_massa:
                melhor_massa = massa
                melhor_configuracao = section

    return melhor_configuracao, melhor_massa

if __name__ == "__main__":
    results = calculate_inertia_per_section(sectionsRetangular)
    results = calculate_bending_stress(results=results, M=-0.00009091877047)
    results = calculate_mass(results, sectionsRetangular, BALSA)
    print(json.dumps(results, indent=4, default=float))

    print("")
    print("============================")
    print("============================")
    print("============================")
    print("============================")
    print("")

    results = calculate_inertia_per_section(sectionsCircular)
    results = calculate_bending_stress(results=results, M=-0.00009091877047)
    results = calculate_mass(results, sectionsCircular, FIBRA_CARBONO)
    print(json.dumps(results, indent=4, default=float))