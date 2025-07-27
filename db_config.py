# MARCOS V. SOUSA

import mysql.connector
from dotenv import load_dotenv
import os

        
class db_Config:
    def __init__(self):

        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")


        self.conn = mysql.connector.connect(
                host=db_host, 
                user=db_user,
                password=db_password,
                database=db_database
            )

        self.cursor = self.conn.cursor(dictionary=True)

    def Executar(self, sql, valor=None, commit=False):
        self.cursor.execute(sql, valor)
        if commit:
            self.conn.commit()

        
    
    def Return_Pessoas(self):
        self.Executar("SELECT * FROM Pessoa")
        return self.cursor.fetchall()
    
    def Return_Contas(self):
        self.Executar("SELECT * FROM Conta")
        return self.cursor.fetchall()
    
    def Return_Enderecos(self):
        self.Executar("SELECT * FROM Endereco")
        return self.cursor.fetchall()
    
    def Mudar_Saldo(self, valor_Total, id):
        self.Executar("UPDATE Conta SET Saldo = %s WHERE ID = %s",(valor_Total, id), commit=True)
        return

    def Return_Extrato(self, id_Conta_Login):
        self.Executar("""SELECT t.Tipo, t.Valor, t.Data, t.Conta_Origem, t.Conta_Destino
                    FROM Transacao AS t
                    WHERE t.Conta_Origem = %s OR t.Conta_Destino = %s
                    ORDER BY t.Data DESC;
        """, (id_Conta_Login, id_Conta_Login))
        return self.cursor.fetchall()
    
    def Return_Todas_Transacoes(self):
        self.Executar("""SELECT t.Tipo, t.Valor, t.Data, p1.Nome AS Quem_Fez, p2.Nome AS Quem_Recebeu
                        FROM Transacao AS t
                        LEFT JOIN Conta AS c1 ON t.Conta_Origem = c1.ID
                        LEFT JOIN Pessoa AS p1 ON c1.Pessoa_ID = p1.ID
                        LEFT JOIN Conta AS c2 ON t.Conta_Destino = c2.ID
                        LEFT JOIN Pessoa AS p2 ON c2.Pessoa_ID = p2.ID
                        WHERE t.Tipo IN ('TRANSFERENCIA PIX', 'TRANSFERENCIA BANCARIA')
                        ORDER BY t.Data DESC;
        """)
        return self.cursor.fetchall()

    def Return_Transacoes_Por_Periodo(self, data_Inicial, data_Final):
        self.Executar("""SELECT p.Nome, SUM(t.Valor) AS Total_Movimentado
                    FROM Transacao AS t
                    INNER JOIN Conta AS c ON c.ID = t.Conta_Origem
                    INNER JOIN Pessoa AS p ON p.ID = c.Pessoa_ID
                    WHERE t.Data BETWEEN %s AND %s
                    GROUP BY p.Nome
                    ORDER BY Total_Movimentado
        """, (data_Inicial, data_Final))
        return self.cursor.fetchall()
    
    def Return_Todos_Saldos(self):
        self.Executar("""SELECT c.ID, c.Saldo, p.Nome AS Nome_Titular, p.CPF AS CPF_Titular
                    FROM Pessoa AS p
                    INNER JOIN Conta AS c ON p.ID = c.Pessoa_ID
        """)
        return self.cursor.fetchall()
    
    def Return_Top5(self):
        self.Executar("""SELECT c.ID, c.Saldo, p.Nome AS Nome_Titular, p.CPF AS CPF_Titular
                    FROM Pessoa AS p
                    INNER JOIN Conta AS c ON p.ID = c.Pessoa_ID
                    LIMIT 5
        """)
        return self.cursor.fetchall()
    
    def Return_Saldo_Menor_100(self):
        self.Executar("""SELECT c.ID, c.Saldo, p.Nome AS Nome_Titular, p.CPF AS CPF_Titular
                    FROM Conta AS c
                    INNER JOIN Pessoa AS p ON c.Pessoa_ID = p.ID
                    WHERE c.Saldo < 100
                    """)
        return self.cursor.fetchall()
    
    def Return_Circulacao(self):
        self.Executar("""SELECT SUM(Saldo) AS Dinheiro_em_Circulacao
                    FROM Conta
        """)
        return self.cursor.fetchone()["Dinheiro_em_Circulacao"]
    
    def Return_Pix(self):
        self.Executar("""SELECT t.Tipo, t.Valor, t.Data, p1.Nome AS Quem_Fez, p2.Nome AS Quem_Recebeu
                    FROM Transacao AS t
                    LEFT JOIN Conta AS c1 ON t.Conta_Origem = c1.ID
                    LEFT JOIN Pessoa AS p1 ON c1.Pessoa_ID = p1.ID
                    LEFT JOIN Conta AS c2 ON t.Conta_Destino = c2.ID
                    LEFT JOIN Pessoa AS p2 ON c2.Pessoa_ID = p2.ID
                    WHERE t.Tipo = 'TRANSFERENCIA PIX'
                    ORDER BY t.Data DESC;
        """)
        return self.cursor.fetchall()

    def Return_Quantidade_Transacoes(self):
        self.Executar("""SELECT p.Nome AS Cliente, COUNT(t.ID) AS Quantidade_Transferencias
                    FROM Pessoa AS p
                    INNER JOIN Conta c ON p.ID = c.Pessoa_ID
                    LEFT JOIN Transacao t ON c.ID = t.Conta_Origem AND t.Tipo LIKE 'TRANSFERENCIA%'
                    GROUP BY p.ID, p.Nome
                    ORDER BY Quantidade_Transferencias DESC
        """)
        return self.cursor.fetchall()
    
    def Return_Not_Transacoes(self):
        self.Executar("""SELECT c.ID, c.Saldo, p.Nome AS Nome_Titular, p.CPF AS CPF_Titular
                    FROM Pessoa p
                    INNER JOIN Conta c ON p.ID = c.Pessoa_ID
                    LEFT JOIN Transacao t ON c.ID = t.Conta_Origem
                    WHERE t.ID IS NULL
        """)
        return self.cursor.fetchall()