# MARCOS V. SOUSA

from pessoa import Pessoa
from conta import Conta
from datetime import datetime
from db_config import db_Config

class Sistema:
    def __init__(self):
        self.conexao = db_Config()
        self.conexao.Executar("USE GTech_Banco")

        self.System_Pessoa = Pessoa()
        self.System_Conta = Conta()

    def Pegar_ID_Login(self):
        self.id_Conta_Login = self.System_Conta.Liberar_ID_Login()

    def Verificar_Senha(self,senha):
        if len(senha) == 6 and senha.isnumeric():
            return senha
        else:
            return False

    def Sair(self):
        print("|- Tchau!")
        self.conexao.cursor.close
        self.conexao.conn.close
        exit()                  

    def Depositar(self):
        while True:
            try:
                valor_Deposito = float(input("|- Digite o valor do deposito: R$ "))
                if valor_Deposito <= 0:
                    print("|- Valor invalido!\n|- Tente novamente!")
                    continue
                for conta in self.conexao.Return_Contas():
                    if conta["ID"] == self.id_Conta_Login:
                        valor_Total = float(conta["Saldo"]) + valor_Deposito
                        self.conexao.Mudar_Saldo(valor_Total, self.id_Conta_Login)
                        self.conexao.Executar("INSERT INTO Transacao (Tipo, Valor, Conta_Origem, Conta_Destino) VALUES (%s, %s, NULL, %s)", ("DEPOSITO", valor_Deposito, self.id_Conta_Login), commit=True)
                        print("|- Depositor realizado com sucesso!")
                        return
            except ValueError:
                print("|- Valor invalido!\n|- Tente novamente!")

    def Sacar(self):
        for conta in self.conexao.Return_Contas():
            if conta["ID"] == self.id_Conta_Login:
                if float(conta["Saldo"]) <= 0:
                    print("|- Não dinheiro disponivel para saque!")
                    break
        else:
            while True:
                try:
                    self.Mostrar_Saldo()
                    valor_Sacar = float(input("|- Valor que deseja sacar: R$ "))
                    for conta in self.conexao.Return_Contas():
                        if conta["ID"] == self.id_Conta_Login:
                            if valor_Sacar <= 0 or valor_Sacar > float(conta["Saldo"]):
                                print("|- Valor invalido!\n|- Tente novamente!")
                                continue
                            valor_Total = float(conta["Saldo"]) - valor_Sacar
                            self.conexao.Mudar_Saldo(valor_Total, self.id_Conta_Login)
                            self.conexao.Executar("INSERT INTO Transacao (Tipo, Valor, Conta_Origem, Conta_Destino) VALUES (%s, %s, %s, NULL)", ("SAQUE", valor_Sacar , self.id_Conta_Login), commit=True)
                            print("|- Saque realizado com sucesso!")
                            return
                except ValueError:
                    print("|- Valor invalido!\n|- Tente novamente!")
    
    def Transferencia_Via_Pix(self):
        contas = self.conexao.Return_Contas()

        conta_origem = None
        for conta in contas:
            if conta["ID"] == self.id_Conta_Login:
                conta_origem = conta
                break

        if conta_origem is None:
            print("|- Conta não encontrada!")
            return

        if len(contas) < 2 or float(conta_origem["Saldo"]) <= 0:
            print("|- Não é possível fazer uma transferência")
            return

        while True:
            cpf_destino = self.System_Conta.Validar_CPF("|- Digite a chave pix (CPF) do Destinatário: ")
            self.conexao.Executar("""
                SELECT c.ID 
                FROM Pessoa AS p 
                INNER JOIN Conta AS c ON c.Pessoa_ID = p.ID
                WHERE p.CPF = %s;
                """, (cpf_destino,))
            resultado = self.conexao.cursor.fetchone()

            if resultado is None:
                print("|- Conta não encontrada!\n|- Tente novamente!")
                continue

            id_Conta_Destino = resultado["ID"]
            if id_Conta_Destino == self.id_Conta_Login:
                print("|- Não é possível fazer Pix para a própria conta. Tente novamente.")
                continue
            break

        while True:
            try:
                self.Mostrar_Saldo()
                valor_Pix = float(input("|- Digite o valor do Pix: R$ "))

                if valor_Pix <= 0 or valor_Pix > float(conta_origem["Saldo"]):
                    print("|- Valor inválido!\n|- Tente novamente!")
                    continue

                while True:
                    SouN = input(f"|- Deseja fazer esse pix de R$ {valor_Pix} para a conta de ID {id_Conta_Destino} (S/N): ").strip().upper()
                    if SouN == "S":
                        break
                    elif SouN == "N":
                        return
                    else:
                        print("|- É só S ou N!")
                        continue
                break

            except ValueError:
                print("|- Valor inválido!\n|- Tente novamente!")

        for minha_Conta in contas:
            if minha_Conta["ID"] == self.id_Conta_Login:
                valor_Total_Minha_Conta = float(minha_Conta["Saldo"]) - valor_Pix
                break

        for conta_Destino in contas:
            if conta_Destino["ID"] == id_Conta_Destino:
                valor_Total_Destinatario = float(conta_Destino["Saldo"]) + valor_Pix
                break

        self.conexao.Mudar_Saldo(valor_Total_Minha_Conta, self.id_Conta_Login)
        self.conexao.Mudar_Saldo(valor_Total_Destinatario, id_Conta_Destino)
        self.conexao.Executar(
            "INSERT INTO Transacao (Tipo, Valor, Conta_Origem, Conta_Destino) VALUES (%s, %s, %s, %s)",
            ("TRANSFERENCIA PIX", valor_Pix, self.id_Conta_Login, id_Conta_Destino),
            commit=True
        )
        print("|- Pix realizado com sucesso!")
        return


    def Transferencia_Banco(self):
        contas = self.conexao.Return_Contas()

        conta_origem = None
        for conta in contas:
            if conta["ID"] == self.id_Conta_Login:
                conta_origem = conta
                break

        if conta_origem is None:
            print("|- Conta não encontrada!")
            return

        if len(contas) < 2 or float(conta_origem["Saldo"]) <= 0:
            print("|- Não é possível fazer uma transferência")
            return

        while True:
            try:
                id_Conta_Destino = int(input("|- Digite o ID da conta do Destinatário: "))
                if id_Conta_Destino == self.id_Conta_Login:
                    print("|- Não é possível transferir para a própria conta. Tente novamente.")
                    continue

                self.conexao.Executar("""
                    SELECT * 
                    FROM Conta 
                    WHERE ID = %s;
                    """, (id_Conta_Destino,))
                resultado = self.conexao.cursor.fetchone()

                if resultado is None:
                    print("|- Conta não encontrada!\n|- Tente novamente!")
                    continue
                break
            except ValueError:
                print("|- ID inválido! Digite um número.")

        while True:
            try:
                self.Mostrar_Saldo()
                valor_Transferencia = float(input("|- Digite o valor da transferencia: R$ "))

                if valor_Transferencia <= 0 or valor_Transferencia > float(conta_origem["Saldo"]):
                    print("|- Valor inválido!\n|- Tente novamente!")
                    continue

                while True:
                    SouN = input(f"|- Deseja fazer essa tranferencia de R$ {valor_Transferencia} para a conta de ID {id_Conta_Destino} (S/N): ").strip().upper()
                    if SouN == "S":
                        break
                    elif SouN == "N":
                        return
                    else:
                        print("|- É só S ou N!")
                        continue
                break

            except ValueError:
                print("|- Valor inválido!\n|- Tente novamente!")

        for minha_Conta in contas:
            if minha_Conta["ID"] == self.id_Conta_Login:
                valor_Total_Minha_Conta = float(minha_Conta["Saldo"]) - valor_Transferencia
                break

        for conta_Destino in contas:
            if conta_Destino["ID"] == id_Conta_Destino:
                valor_Total_Destinatario = float(conta_Destino["Saldo"]) + valor_Transferencia
                break

        self.conexao.Mudar_Saldo(valor_Total_Minha_Conta, self.id_Conta_Login)
        self.conexao.Mudar_Saldo(valor_Total_Destinatario, id_Conta_Destino)
        self.conexao.Executar(
            "INSERT INTO Transacao (Tipo, Valor, Conta_Origem, Conta_Destino) VALUES (%s, %s, %s, %s)",
            ("TRANSFERENCIA BANCARIA", valor_Transferencia, self.id_Conta_Login, id_Conta_Destino),
            commit=True
        )
        print("|- Transferencia realizado com sucesso!")
        return
    
    def Mostrar_Saldo(self):
        self.conexao.Executar("SELECT Saldo FROM Conta WHERE ID = %s", (self.id_Conta_Login,))
        print(f"|- Saldo: R$ {self.conexao.cursor.fetchone()["Saldo"]}")

        
    def Extrato_Bancario(self):
        extrato = self.conexao.Return_Extrato(self.id_Conta_Login)
        if len(extrato) == 0:
            print("|- Não foi efetuada nenhuma trasação!")
            return
        else:
            for transacao in extrato:
                print("\n========-----\n")
                if transacao["Tipo"] == "TRANSFERENCIA PIX" or transacao["Tipo"] == "TRANSFERENCIA BANCARIA":
                    if transacao["Conta_Destino"] == self.id_Conta_Login:
                        self.conexao.Executar("""SELECT p.Nome
                                            FROM Pessoa AS p
                                            INNER JOIN Conta AS c ON c.Pessoa_ID = p.ID
                                            WHERE c.ID = %s
                                            """,(transacao["Conta_Origem"],))
                        destinatario = self.conexao.cursor.fetchone()["Nome"]
                        print(f"|- Feito por: {destinatario}")
                    else:
                        self.conexao.Executar("""SELECT p.Nome
                                            FROM Pessoa AS p
                                            INNER JOIN Conta AS c ON c.Pessoa_ID = p.ID
                                            WHERE c.ID = %s
                                            """,(transacao["Conta_Destino"],))
                        destinatario = self.conexao.cursor.fetchone()["Nome"]
                        print(f"|- Feito para: {destinatario}")
                print(f"|- Data: {transacao["Data"]}")
                print(f"|- Tipo: {transacao["Tipo"]}")
                print(f"|- Valor: R$ {transacao["Valor"]}")
                print("")
            print("========-----\n")

    def Mudar_Senha(self):
        contas = self.conexao.Return_Contas()
        while True:
            try:
                senha_Atual = str(input("|- Digite sua senha atual: ")).strip()
            except ValueError:
                print("|- Senha invalida!")
            for conta in contas:
                if conta["ID"] == self.id_Conta_Login and conta["Senha"] == senha_Atual:
                    while True:
                        while True:
                            try:
                                nova_Senha = self.Verificar_Senha(str(input("|- Digite a sua nova senha: ")).strip())
                                if not(nova_Senha):
                                    print("|- Senha invalida! A senha tem que ter exatamente 6 digitos numericos\n|- Tente novamente!")
                                    continue
                                else:
                                    break
                            except ValueError:
                                print("|- Senha invalida!")
                        while True:
                            try:
                                nova_Senha2 = self.Verificar_Senha(str(input("|- Confirme a sua nova senha: ")).strip())
                                if not(nova_Senha2):
                                    print("|- Senha invalida! A senha tem que ter exatamente 6 digitos numericos\n|- Tente novamente!")
                                    continue
                                else:
                                    break
                            except ValueError:
                                print("|- Senha invalida!")
                        
                        if nova_Senha != nova_Senha2:
                            print("|- Confirmação invalida\n|- Tente novamente!")
                            continue

                        elif nova_Senha == senha_Atual:
                            print("|- A nova senha tem que ser diferente da senha antiga!\n|- Tente novamente!")

                        else:
                            self.conexao.Executar("""UPDATE Conta
                                                SET Senha = %s
                                                WHERE ID = %s""", (nova_Senha, self.id_Conta_Login), commit=True)
                            print("|- Senha alterada com sucesso!")
                            return
                        
    """
    - Número de transferências realizadas por cliente - contagem (COUNT) agrupada por cliente.
    - Clientes que nunca realizaram transações (clientes inativos) - INNER JOIN entre cliente e transações, onde o campo de transação para o cliente seja NULL.
    """
                        
    def Mostrar_Todas_Transacoes(self):
        transacoes = self.conexao.Return_Todas_Transacoes()

        if len(transacoes) == 0:
            print("|- Nenhuma transferencia foi realizada!")
            return

        for transacao in transacoes:
            quem_fez = transacao['Quem_Fez'] if transacao['Quem_Fez'] else "Desconhecido"
            quem_recebeu = transacao['Quem_Recebeu'] if transacao['Quem_Recebeu'] else "Desconhecido"


            print("\n========-----\n")
            print(f"|- Data: {transacao["Data"]}")
            print(f"|- Tipo: {transacao["Tipo"]}")
            print(f"|- Valor: R$ {transacao["Valor"]}")
            print(f"|- Quem fez: {quem_fez}")
            print(f"|- Quem recebeu: {quem_recebeu}")
        print("\n========-----\n")

    def Mostrar_Transacoes_Por_Periodo(self):
        while True:
            data_inicio = str(input("|- Digite a data inicial (AAAA-MM-DD): ")).strip()
            try:
                datetime.strptime(data_inicio, "%Y-%m-%d")
                break
            except ValueError:
                print("|- Formato inválido! Use AAAA-MM-DD")

        while True:
            data_fim = str(input("|- Digite a data final (AAAA-MM-DD): ")).strip()
            try:
                datetime.strptime(data_fim, "%Y-%m-%d")
                if data_fim < data_inicio:
                    print("|- A data final deve ser igual ou posterior à data inicial")
                else:
                    break
            except ValueError:
                print("|- Formato inválido! Use AAAA-MM-DD")

        data_inicio = data_inicio + " 00:00:00"
        data_fim = data_fim + " 23:59:59"

        transacoes = self.conexao.Return_Transacoes_Por_Periodo(data_inicio, data_fim)

        if len(transacoes) == 0:
            print("|- Nenhuma movimentação foi realizada nesse periodo!")
            return

        print(f"\n|- Relatório de movimentade dinheiro de {data_inicio} até {data_fim}:")

        for transacao in transacoes:
            print("\n========-----\n")
            print(f"|- Cliente: {transacao["Nome"]}")
            print(f"|- Total movimentado: R$ {transacao["Total_Movimentado"]:.2f}")
        print("\n========-----\n")

    def Return_Saldo_Todas_Contas(self):
        contas = self.conexao.Return_Todos_Saldos()
        if len(contas) == 0:
            print("|- Nenhuma conta cadastrada!")
            return
        
        else:
            for conta in contas:
                print("\n========-----\n")
                print(f"|- ID Conta: {conta["ID"]}")
                print(f"|- Saldo: R$ {float(conta["Saldo"])}")
                print(f"|- Nome Titular: {conta["Nome_Titular"]}")
                print(f"|- CPF Titular: {conta["CPF_Titular"]}")
            print("\n========-----\n")

    def Top_Cinco(self):
        contas = self.conexao.Return_Todos_Saldos()
        if len(contas) == 0:
            print("|- Nenhuma conta cadastrada!")
            return

        contas_ordenadas = sorted(contas, key=lambda x: float(x["Saldo"]), reverse=True)[:5]
        top = 0
        for conta in contas_ordenadas:
            top += 1
            print("\n========-----\n")
            print(f"|- {top}º ->")
            print(f"|- ID Conta: {conta["ID"]}")
            print(f"|- Saldo: R$ {float(conta["Saldo"])}")
            print(f"|- Nome Titular: {conta["Nome_Titular"]}")
            print(f"|- CPF Titular: {conta["CPF_Titular"]}")
        print("\n========-----\n")

    def Menor_100(self):
        contas = self.conexao.Return_Saldo_Menor_100()
        if len(contas) == 0:
            if len(self.conexao.Return_Contas()) == 0:
                print("|- Nenhuma conta cadastrada!")
                return
            print("|- Não há nenhuma conta com saldo menor que R$ 100!")
            return
        
        else:
            for conta in contas:
                print("\n========-----\n")
                print(f"|- ID Conta: {conta["ID"]}")
                print(f"|- Saldo: R$ {float(conta["Saldo"])}")
                print(f"|- Nome Titular: {conta["Nome_Titular"]}")
                print(f"|- CPF Titular: {conta["CPF_Titular"]}")
            print("\n========-----\n")

    def Valor_Em_Circulação(self):
        dinheiro_Circulacao = self.conexao.Return_Circulacao()
        if dinheiro_Circulacao is None:
            dinheiro_Circulacao = 0.0
        print(f"|- Dinheiro circulando: R$ {dinheiro_Circulacao}")

    def Mostrar_Todas_Transacoes_Pix(self):
        transacoes = self.conexao.Return_Pix()

        if len(transacoes) == 0:
            print("|- Nenhuma transferencia via pix foi realizada!")
            return

        for transacao in transacoes:
            quem_fez = transacao['Quem_Fez'] if transacao['Quem_Fez'] else "Desconhecido"
            quem_recebeu = transacao['Quem_Recebeu'] if transacao['Quem_Recebeu'] else "Desconhecido"


            print("\n========-----\n")
            print(f"|- Data: {transacao["Data"]}")
            print(f"|- Tipo: {transacao["Tipo"]}")
            print(f"|- Valor: R$ {transacao["Valor"]}")
            print(f"|- Quem fez: {quem_fez}")
            print(f"|- Quem recebeu: {quem_recebeu}")
        print("\n========-----\n")

    def Numero_Transferencias(self):
        clientes = self.conexao.Return_Quantidade_Transacoes()
        if len(clientes) == 0:
            print("|- Nenhuma transferencia foi realizada!")
            return
        else:
            for cliente in clientes:
                print("\n========-----\n")
                print(f"|- Cliente: {cliente["Cliente"]}")
                print(f"|- Quantidade de transferencias feitas: {cliente["Quantidade_Transferencias"]}")
            print("\n========-----\n")

    def Cliente_Not_Transacao(self):
        clientes = self.conexao.Return_Not_Transacoes()
        if len(clientes) == 0:
            if len(self.conexao.Return_Contas()) == 0:
                print("|- Nenhuma conta cadastrada!")
                return
            print("|- Todos clientes fizeram alguma transferencias!")
            return
        else:
            for cliente in clientes:
                print("\n========-----\n")
                print(f"|- ID Conta: {cliente["ID"]}")
                print(f"|- Saldo: R$ {float(cliente["Saldo"])}")
                print(f"|- Nome Titular: {cliente["Nome_Titular"]}")
                print(f"|- CPF Titular: {cliente["CPF_Titular"]}")
            print("\n========-----\n")
