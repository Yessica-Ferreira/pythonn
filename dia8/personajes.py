class Personaje:
    def __init__(self):
        self.habilidad = ["ninguno"]
        
    def atacar(self):
        return "Dar patada"
    
class Guerrero(Personaje):
    def __init__(self):
        super().__init__()
        self.habilidad.append("Combate cuerpo a cuerpo")
        
    def atacar(self):
        return "Atacar con espada"
    
class Mago(Personaje):
    def __init__(self):
        super().__init__()
        self.habilidad.append("Magia nivel 1")
        
    def atacar(self):
        return "Atacar con hechizo"    

class Maestro(Guerrero, Mago):
    
    def atacar(self):
        return "Atacar con espada de fuego y hechizo"
    
guerrero = Guerrero()
mago = Mago()
maestro = Maestro()    

print(guerrero.habilidad)
print(mago.habilidad)
print(maestro.habilidad)

print(guerrero.atacar())  
print(mago.atacar())    
print(maestro.atacar())
    
            