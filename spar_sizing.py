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
