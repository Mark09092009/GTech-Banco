# MARCOS V. SOUSA

from banco import Sistema

class Menus:
    def __init__(self):
        self.Sistema_Banco = Sistema()

    def Menu_Main(self):
        while True:
            print("|>--- MENU MAIN           |")
            print("| 1. Depositar            |")      
            print("| 2. Sacar                |")      
            print("| 3. Tranferencia         |")
            print("| 4. Saldo                |")  
            print("| 5. Extratos             |")  
            print("| 6. Alterar senha        |")  
            print("| 0. Sair                 |")
            print("+-------------------------+")
            opc = str(input("|- Digite a opção desejada: ")).strip()

            match opc:
                case "1":
                    self.Sistema_Banco.Depositar()

                case "2":
                    self.Sistema_Banco.Sacar()

                case "3":
                    self.Menu_Transferencia()

                case "4":
                    self.Sistema_Banco.Mostrar_Saldo()

                case "5":
                    self.Sistema_Banco.Extrato_Bancario()

                case "6":
                    self.Sistema_Banco.Mudar_Senha()

                case "0":
                    return

                case _:
                    print("|- Opção invalida!")

    def Menu_Inicial(self):
        while True:
            print("|>--- MENU INICIAL              |")
            print("| 1. Entrar                     |")
            print("| 2. Criar Conta                |")
            print("| 3. Cadastrar                  |")
            print("| 4. Menu Inutil                |")
            print("| 0. Sair                       |")
            print("+-------------------------------+")
            opc = str(input("|- Digite a opção desejada: ")).strip()

            match opc:
                case "1":
                    
                    if self.Sistema_Banco.System_Conta.Entrar_na_Conta():
                        self.Sistema_Banco.Pegar_ID_Login()
                        self.Menu_Main()
                    else:
                        print("|- Falha no login!\n|- Tente novamente!")

                case "2":
                    self.Sistema_Banco.System_Conta.Criar_Conta()

                case "3":
                    self.Sistema_Banco.System_Pessoa.Cadastrar_Pessoa()

                case "4":
                    self.Menu_Inutil()

                case "0":
                    self.Sistema_Banco.Sair()

                case _:
                    print("|- Opção invalida!")

    def Menu_Transferencia(self):
        while True:
            print("|>- MENU TRANSAÇÕES |")
            print("| 1. Pix            |")
            print("| 2. Bancaria       |")
            print("| 0. Sair           |")
            print("+-------------------+")
            opc = str(input("|- Digite a opção desejada: ")).strip()

            match opc:
                case "1":
                    self.Sistema_Banco.Transferencia_Via_Pix()

                case "2":
                    self.Sistema_Banco.Transferencia_Banco()

                case "0":
                    return
                
                case _:
                    print("|- Opção invalida!")

    def Menu_Inutil(self):
        while True:
            print("|>--- MENU INUTIL                         |")
            print("| 1. Todas Transações                     |")
            print("| 2. Dinheiro Movido Entre Periodos       |")
            print("| 3. Saldos De Todas Contas               |")
            print("| 4. Top Cinco                            |")
            print("| 5. Saldos Menor Que 100                 |")
            print("| 6. Dinheiro Em Circulação               |")
            print("| 7. Todos Pix Realizados                 |")
            print("| 8. Quantidade De Transferencias         |")
            print("| 9. Cliente Que Não Fizeram Transações   |")
            print("| 0. Sair                                 |")
            print("+-----------------------------------------+")
            opc = str(input("|- Digite a opção desejada: ")).strip()

            match opc:
                case "1":
                    self.Sistema_Banco.Mostrar_Todas_Transacoes()
                
                case "2":
                    self.Sistema_Banco.Mostrar_Transacoes_Por_Periodo()

                case "3":
                    self.Sistema_Banco.Return_Saldo_Todas_Contas()

                case "4":
                    self.Sistema_Banco.Top_Cinco()

                case "5":
                    self.Sistema_Banco.Menor_100()

                case "6":
                    self.Sistema_Banco.Valor_Em_Circulação()

                case "7":
                    self.Sistema_Banco.Mostrar_Todas_Transacoes_Pix()

                case "8":
                    self.Sistema_Banco.Numero_Transferencias()

                case "9":
                    self.Sistema_Banco.Cliente_Not_Transacao()

                case "0":
                    return
                
                case _:
                    print("|- Opção invalida!")

if __name__ == "__main__":
    menus = Menus()
    menus.Menu_Inicial()