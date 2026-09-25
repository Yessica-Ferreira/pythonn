import os

import mysql.connector


class ModeloTraduccion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database="BD_TRADUCCIONES_YESSI"
        )

    def agregar_palabra(self, espanol, ingles):
        cursor = self.conexion.cursor()

        sql = """
            INSERT INTO traducciones (palabra_espanol, palabra_ingles)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (espanol, ingles))
        self.conexion.commit()
        cursor.close()

    def buscar_traduccion(self, espanol):
        cursor = self.conexion.cursor()

        sql = """
            SELECT palabra_ingles
            FROM traducciones
            WHERE palabra_espanol = %s
        """

        cursor.execute(sql, (espanol,))
        resultado = cursor.fetchone()
        cursor.close()

        return resultado
