import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO cadastros (id, nome, contato, email, cidade, estado, servico, conteudo, tipo, nota) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('27218064833', 'Fabio Luis', '17991323344', 'fabio@fabio.com.br', 'Jose Bonifacio', 'SP', 'Eletricista', 'Agende seu orçamento sem compromisso', 'A', '0')
            )
connection.commit()
connection.close()