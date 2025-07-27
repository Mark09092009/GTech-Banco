# MARCOS V. SOUSA

DROP DATABASE GTech_Banco;
CREATE DATABASE IF NOT EXISTS GTech_Banco;
USE GTech_Banco;

CREATE TABLE IF NOT EXISTS Endereco (
	ID INT PRIMARY KEY AUTO_INCREMENT,
	CEP VARCHAR(9) NOT NULL,
    Rua VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Pessoa (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(60) NOT NULL,
    CPF VARCHAR(14) NOT NULL UNIQUE,
    Telefone VARCHAR(11),
    Endereco_ID INT,
    FOREIGN KEY (Endereco_ID) REFERENCES Endereco(ID)
		ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Conta (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Senha VARCHAR(6) NOT NULL,
    Saldo DECIMAL(10, 2) NOT NULL,
    Pessoa_ID INT,
    FOREIGN KEY (Pessoa_ID) REFERENCES Pessoa(ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) AUTO_INCREMENT = 1001;

CREATE TABLE IF NOT EXISTS Transacao (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Tipo ENUM('SAQUE','DEPOSITO','TRANSFERENCIA PIX', 'TRANSFERENCIA BANCARIA') NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Conta_Origem INT,
    Conta_Destino INT,
    FOREIGN KEY (Conta_Origem) REFERENCES Conta(ID) ON DELETE CASCADE,
    FOREIGN KEY (Conta_Destino) REFERENCES Conta(ID) ON DELETE CASCADE
);

# Selects que usei para teste!

SELECT t.Tipo, t.Valor, t.Data, p1.Nome AS Quem_Fez, p2.Nome AS Quem_Recebeu
FROM Transacao AS t
LEFT JOIN Conta AS c1 ON t.Conta_Origem = c1.ID
LEFT JOIN Pessoa AS p1 ON c1.Pessoa_ID = p1.ID
LEFT JOIN Conta AS c2 ON t.Conta_Destino = c2.ID
LEFT JOIN Pessoa AS p2 ON c2.Pessoa_ID = p2.ID
WHERE t.Tipo IN ('TRANSFERENCIA PIX', 'TRANSFERENCIA BANCARIA')
ORDER BY t.Data DESC;

SELECT c.ID AS ID_Conta, p.CPF AS CPF_Titular
FROM Pessoa AS p
INNER JOIN Conta AS c ON c.Pessoa_ID = p.ID;

SELECT t.Tipo, t.Valor, t.Data, t.Conta_Origem, t.Conta_Destino
FROM Transacao AS t
INNER JOIN Conta AS c ON c.ID = t.Conta_Origem OR c.ID = t.Conta_Destino
WHERE c.ID = ?;

SELECT p.Nome, c.Saldo
FROM Pessoa AS p
INNER JOIN Conta AS c ON p.ID = c.Pessoa_ID;

SELECT t.Tipo, t.Valor, t.Data,p1.Nome AS Quem_Fez,p2.Nome AS Quem_Recebeu
FROM Transacao AS t
INNER JOIN Conta AS c1 ON t.Conta_Origem = c1.ID
INNER JOIN Pessoa AS p1 ON c1.Pessoa_ID = p1.ID
INNER JOIN Conta AS c2 ON t.Conta_Destino = c2.ID
INNER JOIN Pessoa AS p2 ON c2.Pessoa_ID = p2.ID
WHERE t.Tipo IN ('TRANSFERENCIA PIX', 'TRANSFERENCIA BANCARIA')
ORDER BY t.Data DESC;

SELECT SUM(Saldo) AS Dinheiro_em_Circulacao
FROM Conta;

SELECT ID, Saldo
FROM Conta
ORDER BY Saldo DESC
LIMIT 5;

SELECT p.Nome, SUM(t.Valor) AS Total_Movimentado
FROM Transacao AS t
INNER JOIN Conta AS c ON c.ID = t.Conta_Origem
INNER JOIN Pessoa AS p ON p.ID = c.Pessoa_ID
GROUP BY p.Nome
ORDER BY Total_Movimentado;

SELECT * FROM Endereco;
SELECT * FROM Pessoa;
SELECT * FROM Conta;
SELECT * FROM Transacao;
SHOW TABLES;