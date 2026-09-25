# Trabajos del curso de Python

Este repositorio contiene las prácticas realizadas durante el curso,
organizadas en carpetas por día.

## Contenido principal

- `dia1` a `dia16`: ejercicios de Python, interfaces, bases de datos y web.
- `dia15/app2`: inventario desarrollado con Django y MySQL.
- `dia18/appBlog`: blog desarrollado con Django y SQLite.
- `dia18/practica_final`: ejercicios finales, detector de palabras y juego con Pygame.

## Bases de datos incluidas

- `dia12/traductor/BD_TRADUCCIONES_YESSI.sql`
- `dia15/app2/app2_db_estructura.sql`
- `dia15/app2/app2_productos.sql`
- `dia18/appBlog/db.sqlite3`

Las contraseñas reales no se guardan en GitHub. En PowerShell se pueden
configurar antes de ejecutar los proyectos:

```powershell
$env:MYSQL_PASSWORD = "tu_contraseña_de_mysql"
$env:DJANGO_SECRET_KEY = "una_clave_local"
$env:GEMINI_API_KEY = "tu_clave_de_gemini"
```

## Restaurar las bases MySQL desde Git Bash

```bash
mysql -u root -p < dia12/traductor/BD_TRADUCCIONES_YESSI.sql
mysql -u root -p < dia15/app2/app2_db_estructura.sql
mysql -u root -p app2_db < dia15/app2/app2_productos.sql
```

## Ejercicio de clonación

Para el ejercicio de clonar un repositorio externo se utilizó:

```bash
git clone https://github.com/mx0c/super-mario-python.git
```

El código externo no se volvió a publicar dentro de este repositorio.
