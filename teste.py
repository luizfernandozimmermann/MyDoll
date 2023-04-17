from mysql.connector import connect

print("Conectando...")
database = connect(
    host="192.168.0.168",
    user="mydolladmin",
    passwd="polentinho",
    port = "3306",
    database="mydoll"
)
print("Conectado")
cursor = database.cursor()

cursor.execute("SHOW TABLES")
tabelas = list(map(lambda x: x[0], cursor.fetchall()))
cursor.execute("INSERT INTO colecoes_estoque (colecao, ativo) VALUES ('bonecas', 1)")
resultado = []
for tabela in tabelas:
    cursor.execute(f"SELECT * FROM {tabela}")
    resultado.append(cursor.fetchall())

database.commit()

print(resultado)