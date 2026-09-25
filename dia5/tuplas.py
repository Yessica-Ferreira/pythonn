sucursal_a = (-25.2637,-57.5759)
sucursal_b = (-25.2968,-57.6350)

latitud_a, longitud_a = sucursal_a
latitud_b, longitud_b = sucursal_b

distancia = ((latitud_b - latitud_a)**2 + (longitud_b - longitud_a)**2) ** (0.5)

print(f"La distancia entre la sucursal A y la sucursal B es: {distancia:.2f} grados")
