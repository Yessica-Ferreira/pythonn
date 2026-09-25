producto = {
    "nombre": "Arroz",
    "precio": 6500,
    "stock": 120
}

cantidad_vendida = 15
producto["stock"] = producto["stock"] - cantidad_vendida    
total = producto["precio"] * cantidad_vendida

print(f"Venta Registrada: {cantidad_vendida} unidades de {producto['nombre']}")
print(f"Total de la venta: Gs. {total}")
print(f"Stock restante: {producto['stock']} unidades")