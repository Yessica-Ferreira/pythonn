# La clase tiene atributos, construtores y métodos
class Producto:
    nombre = None
    
    def __init__(self, n):
        self.nombre = n
        
    def ver_datos(self):
        return f"Producto: {self.nombre}"   
    
#crear un objeto de la clase Producto

p1 = Producto("computadora")
print(p1.ver_datos())    
        
        