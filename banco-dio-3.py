# Versão do meu código com a implementação de Classes
# A versão do curso achei muito complicada e difícil de entender
# Preciso revisar esse código e fazer algumas melhorias, mas vou upar ele assim para dar tempo de terminar o curso a tempo

class Conta:
    def __init__(self, tipo):
        if tipo == 1:
            self.dados = {
                "AGENCIA": "0001",
                "saldo": 0,
                "numero_saques": 0,
                "extrato": '',
                "LIMITE_VALOR": 500,
                "LIMITE_SAQUES": 3
            }
        elif tipo == 2:
            self.dados = {
                "AGENCIA": "0001",
                "saldo": 0,
                "numero_saques": 0,
                "extrato": '',
                "LIMITE_VALOR": 2000,
                "LIMITE_SAQUES": 10
            }

    def depositar(self, valor):
        if valor <= 0:
            print('Valor inválido! O valor deve ser maior que zero.')
        else:
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
            self.dados["saldo"] += valor
            self.dados["extrato"] += f"Depósito: R${valor:.2f}\n"

    def sacar(self, valor):
        if self.dados["numero_saques"] >= self.dados["LIMITE_SAQUES"]:
            print("Você já atingiu o limite diário de saques.")
        elif valor <= 0:
            print("Valor inválido! Tente novamente.")
        elif valor > self.dados["saldo"]:
            print("Saldo insuficiente para operação.")
        elif valor > self.dados["LIMITE_VALOR"]:
            print("Valor de saque excedeu o limite.")
        else:
            print(f"Saque de R${valor:.2f} efetuado com sucesso!")
            self.dados["saldo"] -= valor
            self.dados["extrato"] += f"Saque: R${valor:.2f}\n"
            self.dados["numero_saques"] += 1

    def exibir_extrato(self):
        print("------------- Extrato -------------\n")
        print(self.dados["extrato"] if self.dados["extrato"]
              else "* Não houve operação até o momento *")
        print(f"|| Saldo atual: R${self.dados["saldo"]:.2f} ||")
        print(f"|| Saques realizados: {self.dados["numero_saques"]} de {
              self.dados["LIMITE_SAQUES"]} ||")
        print("-----------------------------------")


class Cliente:
    def __init__(self, nome, data_de_nascimento, cpf, endereco):
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Banco:
    def __init__(self):
        self.clientes = {}

    def cadastrar_cliente(self, cpf, nome, data_de_nascimento, logradouro, nro, bairro, cidade, estado):
        if cpf in self.clientes:
            print("CPF já cadastrado. Não é possível cadastrar novamente")
            return

        endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}"
        novo_cliente = Cliente(nome, data_de_nascimento, cpf, endereco)
        self.clientes[cpf] = novo_cliente
        print("Cliente cadastrado com sucesso!")
        print(vars(novo_cliente))

    def abrir_conta(self, cpf, tipo_conta):
        if cpf not in self.clientes:
            print("Cliente não cadastrado. Por favor, cadastre o cliente primeiro.")
            return

        cliente = self.clientes[cpf]
        conta_nova = Conta(tipo_conta)
        cliente.adicionar_conta(conta_nova)
        print("Conta aberta com sucesso!")

    def mostrar_clientes(self):
        for cpf, cliente in self.clientes.items():
            saldos = [f"R${conta.dados['saldo']:.2f}" for conta in cliente.contas]
            print(f"CPF: {cpf}, Nome: {
                  cliente.nome}, Saldos das Contas: {saldos}")

    def selecionar_cliente(self, cpf):
        if cpf in self.clientes:
            print(f"Bem-vindo {self.clientes[cpf].nome}")
            return self.clientes[cpf]
        else:
            print("Cliente não cadastrado ou CPF inválido. Por favor, tente novamente")
            return None

    def selecionar_conta(self, cliente):
        if not cliente:
            print("Nenhum cliente selecionado.")
            return None

        if not cliente.contas:
            print("Este cliente não possui contas.")
            return None

        for i, conta in enumerate(cliente.contas):
            tipo = "Básica" if conta.dados["LIMITE_VALOR"] == 500 else "Premium"
            print(
                f"{i + 1}. Conta {tipo}, Saldo: R${conta.dados['saldo']:.2f}")

        try:
            indice = int(input("Selecione o número da conta: ")) - 1
            if 0 <= indice < len(cliente.contas):
                return cliente.contas[indice]
            else:
                print("Conta inválida.")
                return None
        except ValueError:
            print("Entrada inválida")
            return None

# *** Loop Principal do Programa ***


def main():
    banco = Banco()
    cliente_atual = None
    conta_atual = None

    menu = '''
    ================================= MENU ================================
    *** Operações de Clientes ***      ||   *** Operações de Conta ***
        1.[c]. Castrar Cliente         ||        [d].Depositar 
        2.[n]. Selecionar Cliente      ||        [s].Sacar 
        3.[a]. Abrir Conta             ||        [e].Ver extrato
        4.[o]. Selecionar Conta        ||
        5.[m]. Mostrar Clientes        ||

                                    [x] Sair
    => '''

    while True:
        operacao = input(menu).lower()

        if operacao in ["d", "s", "e", "a"]:
            if not cliente_atual:
                print("Nenhum cliente selecionado.")
                continue

        if operacao in ["d", "s", "e"]:
            if not conta_atual:
                print("Nenhuma conta selecionada")
                continue

        match operacao:
            case "c":
                cpf = input("Digite seu CPF: ")
                nome = input("Digite o nome completo: ").title()
                data_de_nascimento = input(
                    "Digite a data de nascimento (dd/mm/aaaa): ")
                logradouro = input("Digite o logradouro: ").title()
                nro = input("Digite o número do endereço: ")
                bairro = input("Digite o bairro: ").title()
                cidade = input("Digite a cidade: ").title()
                estado = input("Digite o Estado (sigla): ").upper()
                banco.cadastrar_cliente(
                    cpf, nome, data_de_nascimento, logradouro, nro, bairro, cidade, estado)
                cliente_atual = None
                conta_atual = None
            case "a":
                if cliente_atual:
                    tipo_conta = int(
                        input("Escolha o tipo de Conta Corrente (1. Básica | 2. Premium): "))
                    banco.abrir_conta(cliente_atual.cpf, tipo_conta)
            case "d":
                if conta_atual:
                    valor = float(input("Digite o valor do depósito: "))
                    conta_atual.depositar(valor)
            case "s":
                if conta_atual:
                    valor = float(input("Digite o valor do saque: "))
                    conta_atual.sacar(valor)
            case "e":
                if conta_atual:
                    conta_atual.exibir_extrato()
            case "m":
                banco.mostrar_clientes()
            case "n":
                cpf = input("Digite o número do CPF do cliente: ")
                cliente_atual = banco.selecionar_cliente(cpf)
            case "o":
                if cliente_atual:
                    conta_atual = banco.selecionar_conta(cliente_atual)
            case "x":
                break
            case _:
                print("Operação inválida! Selecione uma das opções.")


main()
