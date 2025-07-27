# MARCOS V. SOUSA

class Conta:

    def Verificar_Senha(self,senha):
        if len(senha) == 6 and senha.isnumeric():
            return senha
        else:
            return False

    def Validar_CPF(self,mensagem):
        while True:
            cpf = input(mensagem).strip()

            cpf = cpf.replace(".", "").replace("-", "")

            if not cpf.isdigit() or len(cpf) != 11:
                print("|- Erro! O CPF deve ter exatamente 11 dígitos numéricos")
                continue

            if cpf == cpf[0] * 11: 
                print("|- Erro! CPF inválido")
                continue

            soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
            resto1 = (soma1 * 10) % 11
            if resto1 >= 10:
                resto1 = 0

            soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
            resto2 = (soma2 * 10) % 11
            if resto2 >= 10:
                resto2 = 0

            if int(cpf[9]) == resto1 and int(cpf[10]) == resto2:
                return cpf
            else:
                print("|- Erro! CPF inválido")

    def Liberar_ID_Login(self):
        return self.id_conta_Login

    def Entrar_na_Conta(self):
        from banco import Sistema
        Sistema = Sistema()
        conexao = Sistema.conexao

        if len(conexao.Return_Contas()) == 0:
            print("|- Nenhuma conta cadastrada!")
            return False
        
        try:
            id_Conta = int(input("|- Digite o ID da conta: "))
        except ValueError:
            print("|- ID invalido!")
            return False

        for conta in conexao.Return_Contas():
            if conta["ID"] == id_Conta:
                senha = str(input("|- Digite a senha: ")).strip()
                if conta["Senha"] == senha:
                    print("|- Entrada confirmada!")
                    self.id_conta_Login = conta["ID"]
                    return True
                else:
                    print("|- Senha incorreta!")
                    return False
        else:
            print("|- ID incorreto!")
            return False

    def Criar_Conta(self):
        from banco import Sistema
        Sistema = Sistema()
        conexao = Sistema.conexao

        if len(conexao.Return_Pessoas()) < 1:
            print("|- Não possui pessoas cadastradas!\n|- Tente novamente!")

        else:
            cpf_Titular = self.Validar_CPF("|- Digite o CPF do titular: ")

            if len(conexao.Return_Contas()) >= 1:
                for conta in conexao.Return_Contas():
                    if conta["ID"] == cpf_Titular:
                        print("|- CPF ja cadastrado")
                        return

            for pessoa in conexao.Return_Pessoas():
                if pessoa["CPF"] == cpf_Titular:
                    
                    while True:
                        senha = self.Verificar_Senha(str(input("|- Crie sua senha: ")).strip())
                        if not(senha):
                            print("|- Senha invalida! A senha tem que ter exatamente 6 digitos numericos\n|- Tente novamente!")
                            continue
                        else:
                            break
                    
                    
                    conexao.Executar("INSERT INTO Conta(Senha, Saldo, Pessoa_ID) VALUES (%s, %s, %s)", (senha, 0.0, pessoa["ID"]), commit=True)
                    conexao.Executar("SELECT LAST_INSERT_ID() AS ID")
                    id_Conta = conexao.cursor.fetchone()["ID"]
                    print(f"|- Cadastro {id_Conta} - Realizado com sucesso")
                    break
            else:
                print("|- Nenhuma pessoa com esse CPF esta cadastrada!")
                print("|- Tente novamente!")
                return