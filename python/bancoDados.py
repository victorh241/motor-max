import mysql.connector

def carregarBD():
    conexao = None
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'motormax'
    }
    try:
        conexao = mysql.connector.connect(**db, use_pure=True)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return conexao

def fechar_conecxao():
    cnx = carregarBD()
    if cnx.is_connected():
        cnx.close()