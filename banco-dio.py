# Um programa simples de banco que fornece ao usuário 3 opções: depositar, sacar ou ver o extrato;

MENU = '''
[d] Depositar
[s] Sacar
[e] Ver extrato
[x] Sair

=> '''

saldo = 0
numero_saques = 0
extrato = ''
LIMITE_VALOR = 500
LIMITE_SAQUES = 3


while True:
    operacao = input(MENU).lower()

    match operacao:

        # DEPÓSITO
        case "d":
            valor = float(input("Digite o valor do depósito: "))

            if valor < 0:
                print('Valor inválido! Tente novamente.')
            else:
                print(f"Depósito de R${valor:.2f} realizado com sucesso!")
                saldo += valor
                extrato += f"Depósito: R${valor:.2f}\n"

        # SAQUE
        case "s":
            valor = float(input("Digite o valor do saque: "))

            saque_excedido = numero_saques == LIMITE_SAQUES
            saque_invalido = valor < 0
            saque_insuficiente = valor > saldo
            saque_limite = valor > LIMITE_VALOR

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
                saldo -= valor
                extrato += f"Saque: R${valor:.2f}\n"
                numero_saques += 1

        # EXTRATO
        case "e":
            print("------------- Extrato -------------\n")
            print("* Não houve operação até o momento *" if not extrato else extrato)
            print(f"\n|| Valor atual em conta: R${saldo:.2f} ||")
            print(f"|| Quantidade de saques: {numero_saques} de 3 ||")
            print("-----------------------------------")

        # SAIR
        case "x":
            break
        case _:
            print("Operação inválida! Selecione uma das opções.")
