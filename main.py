import sqlite3

conn = sqlite3.connect('Banco de Dados.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE Pedidos (
        cntr INTEGER PRIMARY KEY,
        status TEXT,
        pedido INTEGER,
        tara INTEGER,
        pesoBruto REAL,
        lacre TEXT,
        armador TEXT,
        booking TEXT,
        terminal TEXT,
        origem TEXT,
        destino TEXT,
        deadlineFabrica DATE,
        deadlinePorto DATE,
        janelaInicio DATE,
        janelaFim DATE,
        cpfMotorista VARCHAR(11),
        motorista TEXT,
        placaCavalo TEXT,
        placaCarreta TEXT
);
""")

conn.close()