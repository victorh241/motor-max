import mysql.connector

def carregarBD():
    conexao = None
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'motormax'
    }
    try:
        conexao = mysql.connector.connect(**db, use_pure=True)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return conexao