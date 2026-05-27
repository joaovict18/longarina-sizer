class SectionRectangular:
    def __init__(self, base, altura, espessura, material):
        self.base = base
        self.altura = altura
        self.espessura = espessura
        self.material = material
        self.type = "retangular"

    def __iter__(self):
        return iter([self])
    
class SectionCircular:
    def __init__(self, diametro_ext, espessura, material):
        self.diametro_ext = diametro_ext
        self.espessura = espessura
        self.material = material
        self.type = "circular"

    def __iter__(self):
        return iter([self])