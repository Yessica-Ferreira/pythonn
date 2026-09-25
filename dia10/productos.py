productos = ["Arroz", "Aceite", "Fideos", "Azúcar"]

with open("productos.txt", "a", encoding="utf-8") as archivo:
    for p in productos:
        archivo.write(f"{p}\n")
        
print("Lista de productos guardada en 'productos.txt'.")    
with open("productos.txt", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    
    for p in lineas:
       print(f"{p.strip()}")
        
        