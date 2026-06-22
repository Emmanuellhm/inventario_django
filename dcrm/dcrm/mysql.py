import mysql.connector

# crea la base de datos "cliente" si no existe y confirma.

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE IF NOT EXISTS cliente")
print("Base de datos creada con exito")





# Si quieres usarlo como helper (opcional):

def get_mysql_connection():
    """Conexión MySQL con mysql.connector (usar si necesitas leer/escribir)."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cliente",
    )
