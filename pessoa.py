# MARCOS V. SOUSA

class Pessoa:
    
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

    def Cadastrar_Pessoa(self):
        from banco import Sistema
        Sistema = Sistema()
        conexao = Sistema.conexao

        while True:
            nome = str(input("|- Digite o nome: ")).title().strip()
            if len(nome) > 60:
                print("|- Tamanho do nome passa do limite de caracteres (60)!")
                continue
            elif len(nome) == 0:
                print("|- Digite algo!!!")
                continue
            break
        while True:
            cpf = self.Validar_CPF("|- Digite seu CPF: ")
            for pessoa in conexao.Return_Pessoas():
                if pessoa["CPF"] == cpf:
                    print("|- CPF ja cadastrado!")
                    break
            else:
                break
            continue
        while True:
            telefone = str(input("|- Digite o telefone (se houver): ")).strip()
            if len(telefone) > 11:
                print("|- Tamanho do telefone passa do limite de caracteres (11)!")
                continue
            break
        while True: 
            cep = str(input("|- Digite o CEP: ")).strip()
            if len(cep) > 9:
                print("|- Tamanho do CEP passa do limite de caracteres (9)!")
                continue
            elif len(cep) == 0:
                print("|- Digite algo!!!")
                continue
            break
        while True:
            rua = str(input("|- Digite a rua: ")).strip().title()
            if len(rua) > 100:
                print("|- Tamanho da rua passa do limite de caracteres (100)!")
                continue
            elif len(rua) == 0:
                print("|- Digite algo!!!")
                continue
            break

        id_Endereco = None

        for endereco in conexao.Return_Enderecos():
            if endereco["CEP"] == cep and endereco["Rua"] == rua:
                id_Endereco = endereco["ID"]
                break
        if id_Endereco is None:
            conexao.Executar("INSERT INTO Endereco(CEP, Rua) VALUES (%s, %s)", (cep, rua), commit=True)
            conexao.Executar("SELECT LAST_INSERT_ID() AS ID")
            id_Endereco = conexao.cursor.fetchone()["ID"]

        conexao.Executar("INSERT INTO Pessoa(Nome, CPF, Telefone, Endereco_ID) VALUES (%s, %s, %s, %s)", (nome, cpf, telefone, id_Endereco), commit=True)
        print("|- Cadastro realizado com sucesso!")