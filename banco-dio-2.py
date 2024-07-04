# Evolução do Projeto Banco Dio
# O programo foi modularizado com funções
# Novas opções no MENU: Cadastrar Cliente, Abrir Conta, Selecionar Cliente, Selecionar Conta
# Adição de 2 tipos de modelos de contas

# Importamos essa biblioteca para fazer um deepcopy de conta básica, caso futuramente adicionarmos um objeto mutável, como uma lista
import copy

# Menu de opções do Programa
menu = '''
================================ MENU ================================
[c].Cadastrar Cliente \t| [a].Abrir Conta

[n].Selecionar Cliente\t| [o].Selecionar Conta | [m].Mostrar Clientes

[d].Depositar \t        | [s].Sacar            | [e].Ver extrato

[x]  Sair

=> '''

# *** Modelos de Contas ***
CONTA_BASICA = {"AGENCIA": "0001",
                "saldo": 0,
                "numero_saques": 0,
                "extrato": '',
                "LIMITE_VALOR": 500,
                "LIMITE_SAQUES": 3}

CONTA_PREMIUM = {"AGENCIA": "0001",
                 "saldo": 0,
                 "numero_saques": 0,
                 "extrato": '',
                 "LIMITE_VALOR": 2000,
                 "LIMITE_SAQUES": 10}

# lista de clientes, com um cliente de modelo
clientes = {
    "123": {
        "nome": "Rafael Antunes Martins",
        "data_de_nascimento": "04/02/1998",
        "cpf": "41577626818",
        "endereco": {
            "logradouro": "Rua Alberto Lanzoni",
            "nro": "982",
            "bairro": "Santa Felícia",
            "cidade": "São Carlos",
            "estado": "SP"},
        "contas": [copy.deepcopy(CONTA_BASICA)]
    }
}

# Funções *****************************************************************

# Define se a conta será básica ou premium
def criar_conta_corrente():
    while True:
        conta_corrente = int(
            input("Escolha o tipo de Conta Corrente (1. Básica | 2. Premium): "))
        if conta_corrente == 1:
            return copy.deepcopy(CONTA_BASICA)
        elif conta_corrente == 2:
            return copy.deepcopy(CONTA_PREMIUM)
        else:
            print(
                "Entrada inválida. Digite (1) para Conta Básica ou (2) para Conta Premium")


# Cadastra um novo usuário e o adiciona à lista de clientes
def cadastrar_usuario(clientes):
    cpf = input("Digite seu CPF: ")

    if cpf in clientes:
        print("CPF já cadastrado. Não é possível cadastrar novamente")
        return

    nome = input("Digite o nome completo: ").title()
    data_de_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")

    logradouro = input("Digite o logradouro: ").title()
    nro = input("Digite o número do endereço: ")
    bairro = input("Digite o bairro: ").title()
    cidade = input("Digite a cidade: ").title()
    estado = input("Digite o Estado (sigla): ").upper()

    endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}"

    novo_cliente = {
        "nome": nome,
        "data_de_nascimento": data_de_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "contas": []}

    clientes[cpf] = novo_cliente
    print("Cliente cadastrado com sucesso!")
    print(novo_cliente)


# Abre uma conta nova para o cliente selecionado
def abrir_conta(cliente):
    print(f"*** Abrindo nova conta no CPF: {cliente["cpf"]}. ***")
    conta_nova = criar_conta_corrente()
    cliente["contas"].append(conta_nova)
    print("Conta aberta com sucesso!")


# Mostra o CPF, nome e saldo das contas de todos os clientes
def mostrar_clientes(clientes):
    for cpf, cliente in clientes.items():
        saldo = [f"R${conta["saldo"]:.2f}" for conta in cliente["contas"]]
        print(f"CPF: {cpf}, Nome: {
              cliente["nome"]}, Saldo das Contas: {saldo}")


def cliente_sem_cadastro():
    print("Cliente não cadastrato ou CPF inválido. Por favor, tente novamente")


# Seleciona o cliente que serão feitas as operações
def selecionar_cliente(clientes):
    cpf = input("Digite o número do CPF do cliente: ")
    if cpf in clientes:
        print(f"Bem-vindo {clientes[cpf]["nome"]}")
        return clientes[cpf]
    else:
        cliente_sem_cadastro()
        return None

# Seleciona dentre as contas do cliente
def selecionar_conta(cliente):
    if not cliente:
        print("Nenhum cliente selecionado.")
        return None

    if not cliente["contas"]:
        print("Este cliente não possui contas.")
        return None

    # Numera as contas do cliente
    for i, conta in enumerate(cliente["contas"]):
        tipo = "Básica" if conta["LIMITE_VALOR"] == 500 else "Premium"
        print(f"{i + 1}. Conta {tipo}, Saldo: R${conta["saldo"]:.2f}")

    try:
        indice = int(input("Selecione o número da conta: ")) - 1
        if 0 <= indice < len(cliente["contas"]):
            return cliente["contas"][indice]
        else:
            print("Conta inválida.")
            return None
    except ValueError:
        print("Entrada inválida")
        return None

# Deposita o valor na conta do cliente
def depositar(conta):
    try:
        valor = float(input("Digite o valor do depósito: "))
        if valor <= 0:
            print('Valor inválido! O valor deve ser maior que zero.')
        else:
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
            conta["saldo"] += valor
            conta["extrato"] += f"Depósito: R${
                valor:.2f}\n"
    except ValueError:
        print("Entrada inválida. Por favor, digite um valor numérico.")


# Saca o valor da conta do cliente
def sacar(conta):
    try:
        valor = float(input("Digite o valor do saque: "))

        saque_excedido = conta["numero_saques"] == conta["LIMITE_SAQUES"]
        saque_invalido = valor <= 0
        saque_insuficiente = valor > conta["saldo"]
        saque_limite = valor > conta["LIMITE_VALOR"]

        if saque_excedido:
            print("Você já atingiu o limite diários de saques.")
        elif saque_invalido:
            print("Valor inválido! Tente novamente.")
        elif saque_insuficiente:
            print("Saldo insuficiente para operação.")
        elif saque_limite:
            print("Valor de saque excedeu o limite.")
        else:
            print(f"Saque de R${valor:.2f} efetuado com sucesso!")
            conta["saldo"] -= valor
            conta["extrato"] += f"Saque: R${valor:.2f}\n"
            conta["numero_saques"] += 1
    except ValueError:
        print("Entrada inválida. Por favor, digite um valor numérico.")


# Exibe o extrato do cliente
def exibir_extrato(conta):
    print("------------- Extrato -------------\n")
    print(conta["extrato"] if conta["extrato"]
          else "* Não houve operação até o momento *")
    print(f"|| Saldo atual: R${conta["saldo"]:.2f} ||")
    print(f"|| Saques realizados: {conta["numero_saques"]} de {
          conta["LIMITE_SAQUES"]} ||")
    print("-----------------------------------")


# *** Loop Principal do Programa ***
def main():
    cliente_atual = None
    conta_atual = None

    while True:
        operacao = input(menu).lower()

        # Verifica se o usuário selecionou uma operação que exige um cliente
        if operacao in ["d", "s", "e", "a"]:
            if not cliente_atual:
                print("Nenhum cliente selecionado.")
                continue

        # Verifica se o usuário selecionou uma operação que exige uma conta
        if operacao in ["d", "s", "e"]:
            if not conta_atual:
                print("Nenhuma conta selecionada")
                continue

        match operacao:
            case "c":
                cadastrar_usuario(clientes)
                cliente_atual = None  # Reseta o cliente atual após cadastrar um novo cliente
                conta_atual = None
            case "a":
                if cliente_atual:
                    abrir_conta(cliente_atual)
            case "d":
                if conta_atual:
                    depositar(conta_atual)
            case "s":
                if conta_atual:
                    sacar(conta_atual)
            case "e":
                if conta_atual:
                    exibir_extrato(conta_atual)
            case "m":
                mostrar_clientes(clientes)
            case "n":
                cliente_atual = selecionar_cliente(clientes)
            case "o":
                if cliente_atual:
                    conta_atual = selecionar_conta(cliente_atual)
            case "x":
                break
            case _:
                print("Operação inválida! Selecione uma das opções.")

main()