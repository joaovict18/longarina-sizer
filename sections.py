class SectionRectangular:
    def __init__(self, base, altura, espessura):
        self.base = base
        self.altura = altura
        self.espessura = espessura
        self.comprimento = 1.0
        self.type = "retangular"

    def __iter__(self):
        return iter([self])
    
class SectionCircular:
    def __init__(self, diametro_ext, espessura):
        self.diametro_ext = diametro_ext
        self.espessura = espessura
        self.comprimento = 1.0
        self.type = "circular"

    def __iter__(self):
        return iter([self])